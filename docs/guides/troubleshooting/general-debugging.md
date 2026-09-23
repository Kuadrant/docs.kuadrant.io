# General Debugging

This is the starting point for troubleshooting Kuadrant. Work through the sections in order — each one narrows down where the problem is before you spend time collecting detailed logs.

For component-specific issues, see the other sections of this guide.

---

## Control plane vs data plane

Kuadrant has two distinct operational layers. Knowing which one to look at first saves significant time.

| Layer | What it does | Signs of a problem here |
|-------|-------------|------------------------|
| **Control plane** | Reconciles policies into configuration — creates AuthConfigs, WasmPlugins, DNS records, Certificates | Policies stuck in non-Ready state; sub-resources not created; component pods crashing |
| **Data plane** | Enforces policies on live traffic — Authorino handles auth per-request, wasm-shim enforces rate limits, Envoy proxies requests | Policy is `Enforced=True` but requests return unexpected status codes or aren't rate-limited |

A policy that shows `Enforced=True` but isn't working as expected is a data plane problem. A policy stuck in `Accepted=False` or `Enforced=False` is a control plane problem.

> **Note on Authorino:** Authorino runs as a long-lived process in `kuadrant-system`, but it is in the data path — it evaluates auth for every individual request. Authorino logs contain both reconciliation activity (AuthConfig loaded/rejected) and per-request auth decisions. When debugging a 401, look at Authorino logs as a data plane source, not just a control plane one.

---

## Component health checklist

Run this first whenever something is broken:

```bash
kubectl get pods -n kuadrant-system
```

All pods should be `Running` with all containers ready:

| Pod | Layer | Description |
|-----|-------|-------------|
| `kuadrant-operator-controller-manager-*` | Control plane | Main operator — manages all policies |
| `limitador-operator-controller-manager-*` | Control plane | Manages the Limitador deployment |
| `dns-operator-controller-manager-*` | Control plane | DNSPolicy enforcement |
| `authorino-*` | Data path | Per-request auth (ext-authz) |
| `limitador-limitador-*` | Data path | Per-request rate limiting |

Check the `Kuadrant` CR status:

```bash
kubectl get kuadrant -A
kubectl describe kuadrant kuadrant -n kuadrant-system
```

Look for `Ready=True` in `.status.conditions`. If `False`, the `reason` and `message` fields explain why.

Check dependency detection — the operator detects installed dependencies at startup and only registers controllers for detected components:

```bash
kubectl get kuadrant kuadrant -n kuadrant-system \
  -o jsonpath='{.status.conditions}' | jq .
```

If a dependency is missing, policies of the affected type will not be reconciled at all.

---

## Policy status conditions

Check this before collecting logs — it tells you immediately whether you have a control plane or data plane problem.

Every Kuadrant policy exposes two conditions:

| Condition | `True` means | `False` means |
|-----------|-------------|---------------|
| `Accepted` | Policy is syntactically valid and attached to an existing target | Target not found, or policy has a validation error |
| `Enforced` | All sub-resources are healthy and the policy is actively enforced | Sub-resources failed to reconcile, or a dependency is not ready |

```bash
# Check all policies across all namespaces
kubectl get authpolicies,ratelimitpolicies,dnspolicies,tlspolicies -A

# Get full status detail on a specific policy
kubectl describe authpolicy <name> -n <namespace>
```

The `status.conditions` block includes `reason` and `message` fields — the `message` almost always identifies the root cause directly.

**Decision point:**
- `Accepted=False` or `Enforced=False` → control plane problem. Go to [Control plane debugging](#control-plane-debugging).
- Both `True` but requests misbehave → data plane problem. Go to [Correlating a request failure](#correlating-a-request-failure).

---

## Correlating a request failure

Use this when a policy shows `Enforced=True` but requests aren't behaving as expected (wrong status code, not rate-limited, auth not triggered, etc.).

Follow this chain — each step either identifies the problem or rules out that layer:

**Step 1 — Envoy access logs (data plane entry point)**

Enable access logs if you haven't already (see [Data plane debugging](#data-plane-debugging)), then tail the sidecar on the affected pod:

```bash
kubectl logs <pod-name> -c istio-proxy -n <namespace> -f
```

Key fields to look for:

| Field | What it tells you |
|-------|------------------|
| `response_code` | What Envoy returned to the client |
| `response_flags` | `UAEX` = rejected by ext-authz (Authorino); `URX` = upstream rate-limited |
| `upstream_cluster` | Where the request was forwarded (or blocked before forwarding) |

If `response_flags` is `UAEX`, move to step 2. If the request reached the upstream but returned a 4xx/5xx from the application, Kuadrant policies may not be involved.

**Step 2 — Authorino logs (auth decisions)**

```bash
kubectl logs deployment/authorino -n kuadrant-system | grep <host-or-request-id>
```

Authorino logs the matched `AuthConfig`, each evaluator that ran, and why a request was denied. If you set `httpHeaderIdentifier` in the `Kuadrant` CR (see [Data plane debugging](#data-plane-debugging)), grep for the header value to find a specific request.

**Step 3 — Limitador counters (rate limit state)**

```bash
# Port-forward to Limitador's HTTP API
kubectl port-forward svc/limitador-limitador -n kuadrant-system 8080:8080

# Check Limitador is up
curl http://localhost:8080/status

# List active counters for a namespace
curl http://localhost:8080/counters/<namespace>
```

If counters exist and are at the limit, the request is being counted correctly. If no counters exist, the wasm-shim may not be sending descriptors — check the WasmPlugin config.

**Step 4 — Sub-resource config**

```bash
# Auth — AuthConfig should exist and be Ready
kubectl get authconfigs -A
kubectl describe authconfig <name> -n kuadrant-system

# Rate limiting — WasmPlugin should exist
kubectl get wasmplugins -A

# DNS
kubectl get dnsrecords -A

# TLS
kubectl get certificates -A
```

If a sub-resource is missing or in an error state, the policy reconciler hit a problem — switch to [Control plane debugging](#control-plane-debugging).

---

## Control plane debugging

Use this when a policy is `Accepted=False`, `Enforced=False`, or a sub-resource (AuthConfig, WasmPlugin, DNSRecord, Certificate) is missing or in an error state.

### Increase log verbosity

There is no single switch across all control plane components — each is configured independently.

**Authorino** — set via the `Authorino` CR:

```bash
kubectl patch authorino authorino -n kuadrant-system \
  --type='merge' -p '{"spec":{"logLevel":"debug"}}'
```

Valid values: `debug`, `info` (default), `error`. Triggers a rolling restart.

**Limitador** — set via the `Limitador` CR:

```bash
kubectl patch limitador limitador -n kuadrant-system \
  --type='merge' -p '{"spec":{"verbosity":3}}'
```

Verbosity levels: `1`=WARN, `2`=INFO, `3`=DEBUG, `4`=TRACE. Remove or set to `0` to revert.

**kuadrant-operator, limitador-operator, dns-operator** — set via env var:

```bash
kubectl set env deployment/kuadrant-operator-controller-manager \
  -n kuadrant-system LOG_LEVEL=debug

kubectl set env deployment/limitador-operator-controller-manager \
  -n kuadrant-system LOG_LEVEL=debug

kubectl set env deployment/dns-operator-controller-manager \
  -n kuadrant-system LOG_LEVEL=debug
```

Each `set env` triggers a rolling restart. Revert with `LOG_LEVEL=info`.

### Useful commands

```bash
# Recent events (sorted by time)
kubectl get events -n kuadrant-system \
  --sort-by='.lastTimestamp' | tail -30

# Watch a policy's status live
kubectl get authpolicy <name> -n <namespace> -w

# Check all Gateway and HTTPRoute attachment status
kubectl get gateways,httproutes -A

# Dump all policy CRs in a namespace
kubectl get authpolicies,ratelimitpolicies,dnspolicies,tlspolicies \
  -n <namespace> -o yaml
```

---

## Data plane debugging

Use this when a policy is `Enforced=True` but requests aren't behaving as expected.

### wasm-shim log verbosity

The wasm-shim runs inside Envoy and logs per-request policy decisions. Configure verbosity via the `Kuadrant` CR:

```yaml
apiVersion: kuadrant.io/v1beta1
kind: Kuadrant
metadata:
  name: kuadrant
  namespace: kuadrant-system
spec:
  observability:
    enable: true
    dataPlane:
      defaultLevels:
        - debug: "true"   # enable debug for all requests
      httpHeaderIdentifier: "x-request-id"  # include this header value in every log line
```

The value of each level entry (`debug`, `info`, `warn`, `error`) is a CEL expression evaluated per request. Use `"true"` to enable unconditionally, or a predicate like `request.headers["x-debug"] == "1"` to enable selectively.

`httpHeaderIdentifier` adds the named header's value to every wasm log line, making it possible to grep for a specific request across logs.

### Envoy access logs

Envoy access logs show proxy-level outcomes for every request — status code, upstream cluster, response flags, and latency — independent of what Kuadrant policies did.

Enable them via an Istio `Telemetry` resource:

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: enable-access-logs
  namespace: istio-system
spec:
  accessLogging:
    - providers:
        - name: envoy
```

Access logs appear in the `istio-proxy` sidecar on workload pods:

```bash
kubectl logs <pod-name> -c istio-proxy -n <namespace> -f
```

Key response flags: `UAEX` (rejected by Authorino), `URX` (rate limited by Limitador).

---

## Key metrics

Enable the Prometheus `ServiceMonitor` resources by setting `observability.enable: true` in the `Kuadrant` CR.

### Control plane health

| Metric | What to check |
|--------|---------------|
| `kuadrant_ready{namespace, name}` | `1` = Kuadrant CR is ready |
| `kuadrant_component_ready{component, namespace}` | `1` = Authorino / Limitador is ready |
| `kuadrant_dependency_detected{dependency}` | `1` = dependency detected at startup. Check `authorino`, `limitador`, `cert-manager`, `dns-operator`, `istio`, `envoygateway` |
| `kuadrant_controller_registered{controller}` | `1` = controller active. `0` for `auth_policies` or `rate_limit_policies` means the dependency was not detected |
| `kuadrant_policies_total{kind}` | Total policies by type |
| `kuadrant_policies_enforced{kind, status="false"}` | Non-zero = policies not enforced — something is wrong |

### Data plane traffic (Istio)

| Metric | What to check |
|--------|---------------|
| `istio_requests_total{response_code="401"}` | Unexpected 401s — AuthPolicy may be denying valid requests |
| `istio_requests_total{response_code="429"}` | Rate limit hits — expected or unexpected? |
| `istio_request_duration_milliseconds` | Latency spike may indicate Authorino or Limitador slowness |

### Limitador health

| Metric | What to check |
|--------|---------------|
| `limitador_up` | `1` = Limitador is running and reachable |

---

## Log collection template

Use this when filing a bug report. Run and share the full output:

```bash
#!/bin/bash
NS=kuadrant-system

echo "=== Kuadrant CR ==="
kubectl get kuadrant -A -o yaml

echo "=== Pod status ==="
kubectl get pods -n $NS -o wide

echo "=== kuadrant-operator logs ==="
kubectl logs deployment/kuadrant-operator-controller-manager -n $NS --tail=200

echo "=== Authorino logs ==="
kubectl logs deployment/authorino -n $NS --tail=200

echo "=== limitador-operator logs ==="
kubectl logs deployment/limitador-operator-controller-manager -n $NS --tail=200

echo "=== Limitador logs ==="
kubectl logs deployment/limitador-limitador -n $NS --tail=200

echo "=== dns-operator logs ==="
kubectl logs deployment/dns-operator-controller-manager -n $NS --tail=200

echo "=== All policies ==="
kubectl get authpolicies,ratelimitpolicies,dnspolicies,tlspolicies -A -o yaml

echo "=== Gateways and HTTPRoutes ==="
kubectl get gateways,httproutes -A -o yaml

echo "=== Sub-resources (control plane output) ==="
kubectl get authconfigs,wasmplugins,dnsrecords,certificates -A -o yaml

echo "=== Recent events ==="
kubectl get events -n $NS --sort-by='.lastTimestamp' | tail -50
```

Open an issue at <https://github.com/Kuadrant/kuadrant-operator/issues/new>.

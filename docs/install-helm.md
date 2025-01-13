# Install with Helm

## Prerequisites

* Kubernetes cluster with support for services of type `LoadBalancer`
* [kubectl CLI](https://kubernetes.io/docs/reference/kubectl/)

## Basic Installation

The latest helm installation instructions for the kuadrant operator are maintained at [https://artifacthub.io/packages/helm/kuadrant/kuadrant-operator](https://artifacthub.io/packages/helm/kuadrant/kuadrant-operator).

After installing the operator, you can create a Kuadrant resource to install the operand components.

```bash
kubectl apply -f - <<EOF
apiVersion: kuadrant.io/v1beta1
kind: Kuadrant
metadata:
  name: kuadrant
  namespace: kuadrant-system
EOF
```

If everything went well, the status of the resource should be `Ready`

```bash
kubectl get kuadrant kuadrant -n kuadrant-system -o=jsonpath='{.status.conditions[?(@.type=="Ready")].message}{"\n"}'
```


## Next Steps

- Try out our [Secure, protect, and connect](kuadrant-operator/doc/user-guides/full-walkthrough/secure-protect-connect.md) guide

#!/bin/bash

kubectl --context kind-mgc-workload-2 delete -f resources/echo-app.yaml
kubectl --context kind-mgc-workload-1 delete -f resources/echo-app.yaml
kubectl --context kind-mgc-control-plane delete -f resources/echo-app.yaml

kubectl delete tlspolicy --all -A
sleep 2
kubectl delete dnspolicy --all -A
sleep 2
kubectl delete dnsrecords --all -A
kubectl delete gateways --all -A

kubectl delete -f resources/gateway_prod-web.yaml
kubectl delete -f ../../../hack/ocm/gatewayclass.yaml
kubectl delete -f resources/placement_http-gateway.yaml
kubectl delete -f resources/managed-cluster-set-binding_gateway-clusters.yaml
kubectl delete -f resources/managed-cluster-set_gateway-clusters.yaml
kubectl --context kind-mgc-control-plane remove -f resources/tlspolicy_prod-web.yaml

kubectl label managedcluster kind-mgc-control-plane ingress-cluster-
kubectl label managedcluster kind-mgc-workload-1 ingress-cluster-
kubectl label managedcluster kind-mgc-workload-2 ingress-cluster-

kubectl label managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-geo-code-
kubectl label managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-geo-code-
kubectl label managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-geo-code-

kubectl label managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-custom-weight-
kubectl label managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-custom-weight-
kubectl label managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-custom-weight-

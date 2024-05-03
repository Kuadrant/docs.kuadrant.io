# This is a vhs (https://github.com/charmbracelet/vhs/) tape - for reproducable CLI recordings

Output dnspolicy.mp4
Set WindowBar Colorful
Set FontSize 25
Set Width 1920
Set Height 1080
Set Framerate 24



Set Shell zsh


Type "kind get clusters"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl label managedcluster kind-mgc-control-plane ingress-cluster=true"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl label managedcluster kind-mgc-workload-1 ingress-cluster=true"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl label managedcluster kind-mgc-workload-2 ingress-cluster=true"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl apply -f resources/managed-cluster-set_gateway-clusters.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl apply -f resources/managed-cluster-set-binding_gateway-clusters.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl apply -f resources/placement_http-gateway.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl create -f ../../../hack/ocm/gatewayclass.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl apply -f resources/gateway_prod-web.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl label gateway prod-web 'cluster.open-cluster-management.io/placement'='http-gateway' -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl --context kind-mgc-control-plane apply -f resources/tlspolicy_prod-web.yaml"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl get managedclusters --show-labels"
Sleep 500ms
Enter
Sleep 5s


Type "cat resources/echo-app.yaml | more"
Sleep 500ms
Enter
Sleep 10s
Type "q"
Enter

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl --context kind-mgc-control-plane apply -f resources/echo-app.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl --context kind-mgc-workload-1 apply -f resources/echo-app.yaml"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl --context kind-mgc-workload-2 apply -f resources/echo-app.yaml"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.200.0'"
Sleep 500ms
Enter
Sleep 5s

Type "curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.201.0'"
Sleep 500ms
Enter
Sleep 5s

Type "curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.202.0'"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl --context kind-mgc-control-plane get gateways -A"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl --context kind-mgc-workload-1 get gateways -A"
Sleep 500ms
Enter
Sleep 5s

Type "kubectl --context kind-mgc-workload-2 get gateways -A"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl get gateway prod-web -n multi-cluster-gateways -o yaml | yq .status"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl --context kind-mgc-control-plane get dnsrecord -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 5s

Type "cat resources/dnspolicy_prod-web-default.yaml"
Sleep 500ms
Enter
Sleep 10s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-default.yaml -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl --context kind-mgc-control-plane get dnsrecord -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl get dnsrecord prod-web-api -n multi-cluster-gateways -o json | jq .spec.endpoints"
Sleep 500ms
Enter
Sleep 5s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "cat resources/dnspolicy_prod-web-weighted.yaml"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-weighted.yaml -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 10s

Hide
Type "clear"
Enter
Show
Sleep 500ms

Type "kubectl label --overwrite managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-custom-weight=AWS"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl label --overwrite managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-custom-weight=AWS"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl label --overwrite managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-custom-weight=GCP"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl get managedclusters --show-labels"
Sleep 500ms
Enter
Sleep 10s

Hide
Type "clear"
Enter
Show
Sleep 500ms

# Show AWS

Type "kubectl label --overwrite managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-geo-code=ES"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl label --overwrite managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-geo-code=DE"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl label --overwrite managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-geo-code=US"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl get managedclusters --show-labels"
Sleep 500ms
Enter
Sleep 10s

Type "cat resources/dnspolicy_prod-web-weighted-geo.yaml"
Sleep 500ms
Enter
Sleep 10s

Type "kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-weighted-geo.yaml -n multi-cluster-gateways"
Sleep 500ms
Enter
Sleep 10s


# https://www.whatsmydns.net/#A/bfa.jm.hcpapps.net
# Bug: Most traffic should go to GCP (WL2, ES)

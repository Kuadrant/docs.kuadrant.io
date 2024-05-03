# We use https://github.com/charmbracelet/vhs to record the terminal session
# For this demo, we have already setup 3 kind Kubernetes clusters. 
# We used the Kuadrant quickstart script to set these up, and to install Kuadrant components and dependencies.
# You can run this too, by running the following:
# export MGC_WORKLOAD_CLUSTERS_COUNT=2; curl https://raw.githubusercontent.com/kuadrant/multicluster-gateway-controller/main/hack/quickstart-setup.sh | bash


kind get clusters
# We have got some local kind clusters: two workload clusters, one OCM Hub/Control Plane

# First, let us label each of these clusters as ingress-clusters which we can place Gateways on
kubectl label managedcluster kind-mgc-control-plane ingress-cluster=true
kubectl label managedcluster kind-mgc-workload-1 ingress-cluster=true
kubectl label managedcluster kind-mgc-workload-2 ingress-cluster=true


# Next, create a ManagedClusterSet with OCM, specifiying a label selector to select the clusters we just labelled with ingress-cluster=true
kubectl apply -f resources/managed-cluster-set_gateway-clusters.yaml

# Now we create a ManagedClusterSetBinding to link the ManagedClusterSet named gateway-clusters to the multi-cluster-gateways namespace
kubectl apply -f resources/managed-cluster-set-binding_gateway-clusters.yaml

# Create a Placement for the ManagedClusterSet, for our 3 clusters
kubectl apply -f resources/placement_http-gateway.yaml

# Create a GatewayClass resource, to specify that Gateways of this class will be managed by the Kuadrant multi-cluster gateway controller
kubectl create -f ../../../hack/ocm/gatewayclass.yaml

# Create a Gateway, called `prod-web`,  (bfa.jm.hcpapps.net)
kubectl apply -f resources/gateway_prod-web.yaml
# Associate the `prod-web` Gateway with the Placement we created earlier
kubectl label gateway prod-web "cluster.open-cluster-management.io/placement"="http-gateway" -n multi-cluster-gateways

# We have already created several OCM resources, such as a ManagedClusterSet for our clusters a Placement for this ManagedClusterSet, and a GatewayClass resource for Kuadrant to utilise our multicluster-gateway-controller
# Create a TLSPolicy
kubectl --context kind-mgc-control-plane apply -f resources/tlspolicy_prod-web.yaml

# Get our ManagedClusters
kubectl get managedclusters --show-labels

# We have got an echo app, which we will deploy to each of our managed clusters
cat resources/echo-app.yaml

# Deploy an echo app to mgc-control-plane, mgc-workload-1 and mgc-workload-2
kubectl --context kind-mgc-control-plane apply -f resources/echo-app.yaml
kubectl --context kind-mgc-workload-1 apply -f resources/echo-app.yaml
kubectl --context kind-mgc-workload-2 apply -f resources/echo-app.yaml

# Check the apps
curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.200.0'
curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.201.0'
curl -k -s -o /dev/null -w '%{http_code}\n' https://bfa.jm.hcpapps.net --resolve 'bfa.jm.hcpapps.net:443:172.31.202.0'

# Check the Gateways
kubectl --context kind-mgc-control-plane get gateways -A
kubectl --context kind-mgc-workload-1 get gateways -A
kubectl --context kind-mgc-workload-2 get gateways -A

# And their status
kubectl get gateway prod-web -n multi-cluster-gateways -o yaml | yq .status

# Look at a simple, RR DNSPolicy
cat resources/dnspolicy_prod-web-default.yaml

# Apply it
kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-default.yaml -n multi-cluster-gateways

# Observe records created
kubectl --context kind-mgc-control-plane get dnsrecord -n multi-cluster-gateways
kubectl get dnsrecord prod-web-api -n multi-cluster-gateways -o json | jq .spec.endpoints

# Setup weighted DNS for specifically labeled clusters
cat resources/dnspolicy_prod-web-weighted.yaml
kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-weighted.yaml -n multi-cluster-gateways

# Label the managedcluster clusters
kubectl label --overwrite managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-custom-weight=AWS
kubectl label --overwrite managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-custom-weight=AWS
kubectl label --overwrite managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-custom-weight=GCP

# Show our labels
kubectl get managedclusters --show-labels

# Show AWS

# Next: Geo + Weighted
# Label the cluster geos
kubectl label --overwrite managedcluster kind-mgc-control-plane kuadrant.io/lb-attribute-geo-code=ES
kubectl label --overwrite managedcluster kind-mgc-workload-1 kuadrant.io/lb-attribute-geo-code=DE
kubectl label --overwrite managedcluster kind-mgc-workload-2 kuadrant.io/lb-attribute-geo-code=US

# Show the labels
kubectl get managedclusters --show-labels

# Show & apply the Geo + Weighted policy
cat resources/dnspolicy_prod-web-weighted-geo.yaml
kubectl --context kind-mgc-control-plane apply -f resources/dnspolicy_prod-web-weighted-geo.yaml -n multi-cluster-gateways


# Show Geo DNS working via https://www.whatsmydns.net/#A/bfa.jm.hcpapps.net

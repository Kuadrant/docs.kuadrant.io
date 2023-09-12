## Getting started with Kuadrant locally

We have a quickstart setup script below which will setup and install Kuadrant and its components (Authorino, Limitador and the Multicluster Gateway Controller) into some local `kind` clusters for evaluation.
### Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Kind](https://kind.sigs.k8s.io/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- OpenSSL >= 3
- AWS account with Route 53 enabled
- [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect) (macOS users only)

### Config

One of Kuadrant's components, the Multicluster Gateway Controller, programs DNS to provide multicluster connectivity and load balaning. As part of setting this up, you'll need to export some environment variables with the keys listed below. Fill in your own values as appropriate. Note that you will need to have created a root domain in AWS using Route 53:

| Env Var                      | Example Value               | Description                                                    |
|------------------------------|-----------------------------|----------------------------------------------------------------|
| `MGC_ZONE_ROOT_DOMAIN`       | `jbloggs.hcpapps.net`       | Hostname for the root Domain                                   |
| `MGC_AWS_DNS_PUBLIC_ZONE_ID` | `Z01234567US0IQE3YLO00`     | AWS Route 53 Zone ID for specified `MGC_ZONE_ROOT_DOMAIN`      | |
| `MGC_AWS_ACCESS_KEY_ID`      | `AKIA1234567890000000`      | Access Key ID, with access to resources in Route 53            |
| `MGC_AWS_SECRET_ACCESS_KEY`  | `Z01234567US0000000`        | Access Secret Access Key, with access to resources in Route 53 |
| `MGC_AWS_REGION`             | `eu-west-1`                 | AWS Region                                                     |
| `MGC_SUB_DOMAIN`             | `myapp.jbloggs.hcpapps.net` | AWS Region                                                     |

>Alternatively, to set defaults, add the above environment variables to your `.zshrc` or `.bash_profile`.

### Set Up Clusters and Kuadrant

   ```bash
  curl https://raw.githubusercontent.com/kuadrant/multicluster-gateway-controller/main/hack/quickstart-setup.sh | bash
   ```

### What's Next

* [Multicluster Gateways walkthrough](how-to/multicluster-gateways-walkthrough.md)
* [Kuadrant Documentation](https://docs.kuadrant.io).
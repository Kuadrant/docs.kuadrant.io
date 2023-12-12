## Kuadrant Getting Started - Single Cluster

## Overview 

In this quick start, we will cover: 
- setup of Kuadrant in a singe local kind cluster

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Kind](https://kind.sigs.k8s.io/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- OpenSSL >= 3
- AWS account with Route 53 enabled or GCP with Cloud DNS enabled
- [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect) (macOS users only)


### DNS Environmental Variables

If you want to make use of the Kuadrant `DNSPolicy` you should setup the following environmental variables depending on your DNS Provider:

### AWS

| Env Var                      | Example Value               | Description                                                                                                 |
|------------------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------|
| `MGC_ZONE_ROOT_DOMAIN`       | `jbloggs.hcpapps.net`       | Hostname for the root Domain                                                                                |
| `MGC_AWS_DNS_PUBLIC_ZONE_ID` | `Z01234567US0IQE3YLO00`     | AWS Route 53 Zone ID for specified `MGC_ZONE_ROOT_DOMAIN`                                                   |
| `MGC_AWS_ACCESS_KEY_ID`      | `AKIA1234567890000000`      | Access Key ID, for user with permissions to Route 53 in the account where root domain is created            |
| `MGC_AWS_SECRET_ACCESS_KEY`  | `Z01234567US0000000`        | Access Secret Access Key, for user with permissions to Route 53 in the account where root domain is created |
| `MGC_AWS_REGION`             | `eu-west-1`                 | AWS Region                                                                                                  |

### GCP

   | Env Var                 | Example Value          | Description                                                    |
   |-------------------------|------------------------|----------------------------------------------------------------|
   | `GOOGLE`     | `{"client_id": "00000000-00000000000000.apps.googleusercontent.com","client_secret": "d-FL95Q00000000000000","refresh_token": "00000aaaaa00000000-AAAAAAAAAAAAKFGJFJDFKDK","type": "authorized_user"}` |  This is the JSON created from either the JSON credentials created by the Google Cloud CLI or a Service account             |
   | `PROJECT_ID` | `my_project_id`   | ID to the google project |
   | `ZONE_NAME`       | `jbloggs-google`   | Zone name                          |
   | `ZONE_DNS_NAME` | `jbloggs.google.hcpapps.net`   | DNS name                        |
   | `LOG_LEVEL`              | `1`                     | Log level for the Controller                          |

>Alternatively, to set defaults, add the above environment variables to your `.zshrc` or `.bash_profile`.

### Set the release you want to use 

```bash
export KUADRANT_REF=v0.6.0
```

### Set Up a kind cluster and install Kuadrant

Run the following:

```bash
curl "https://raw.githubusercontent.com/kuadrant/kuadrant-operator/${KUADRANT_REF}/hack/quickstart-setup.sh" | bash
```
This will setup a single kind cluster, install Istio via the `project sail` operator and install Kuadrant. Once this completes you should be able to move on to using the various policy apis offered by Kuadrant

### What's Next

The next step is to setup and use the policies provided by Kuadrant. 

[Secure, Protect and Connect your Gateway](https://docs.kuadrant.io/kuadrant-operator/docs/how-to/secure-protect-connect/)


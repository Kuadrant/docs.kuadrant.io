# Getting Started

This guide let's you quickly evaluate Kuadrant. You will need a Kubernetes cluster to try out Kuadrant. If you prefer, you can use the following steps to set up a local [kind](https://kind.sigs.k8s.io/) cluster.

## Kind Cluster Setup

```bash
kind create cluster
```

To use Kuadrant, the `LoadBalancer` service type is required for Gateways. kind does not have any built-in way to provide IP addresses to these service types. You can follow this [guide](https://kind.sigs.k8s.io/docs/user/loadbalancer/) to set up a LoadBalancer provider for kind.

## Installation Options

* [Install with Helm](./install-helm.adoc)
* [Install with OLM](./install-olm.md)

## Further Reading

The documentation on this site follows the [Diátaxis framework](https://diataxis.fr/) to better serve you, our users.
This approach also helps us create new content and maintain existing material effectively.
Under this framework, all content falls into one of four categories, accessible from the side navigation:

* Concepts - (also called 'Explanations') Deepens and broadens your understanding of Kuadrant.
* APIs & Reference - Provides concise descriptions of Kuadrant APIs for quick consultation.
* Tutorials - Offers practical, step-by-step activities for you to safely try out.
* Guides - Delivers goal-oriented instructions to help you solve specific problems in any environment.

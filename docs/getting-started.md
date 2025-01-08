# Getting Started

This guide let's you quickly evaluate Kuadrant. You will need a Kubernetes cluster to try out Kuadrant. If you prefer, you can use the following steps to set up a local [kind](https://kind.sigs.k8s.io/) cluster.

## Kind Cluster Setup

```bash
kind create cluster
```

To use Kuadrant, the `LoadBalancer` service type is required for Gateways. kind does not have any built-in way to provide IP addresses to these service types. You can follow this [guide](https://kind.sigs.k8s.io/docs/user/loadbalancer/) to set up a LoadBalancer provider for kind.

## Installation Options

* [Install with Helm](./install-helm.md)
* [Install with OLM](./install-olm.md)

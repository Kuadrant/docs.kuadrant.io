# Overview

Kuadrant combines [Gateway API](https://gateway-api.sigs.k8s.io/) with gateway providers like [Istio](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/) and [Envoy Gateway](https://gateway.envoyproxy.io/) to enhance application connectivity. It enables platform engineers and application developers to easily connect, secure, and protect their services and infrastructure across multiple clusters with policies for [TLS](kuadrant-operator/doc/overviews/tls.md), [DNS](kuadrant-operator/doc/reference/dnspolicy.md), application [authentication & authorization](kuadrant-operator/doc/overviews/auth.md), and [rate limiting](kuadrant-operator/doc/overviews/rate-limiting.md). Additionally, Kuadrant offers [observability templates](kuadrant-operator/doc/observability/examples.md) to further support infrastructure management.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/euWAMvQojP4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Getting Started

For a quick local setup of Kuadrant, see our [Single Cluster](getting-started-single-cluster.md) or [Multi Cluster](getting-started-multi-cluster.md) guides.
Explore the single and multi-cluster architecture in our [Architectural Overview](architecture/docs/design/architectural-overview-v1.md).

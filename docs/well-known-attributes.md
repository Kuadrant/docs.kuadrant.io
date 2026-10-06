# Well-known Attributes

The following tables group well-known attributes by where their values come from. They follow the 1.0.x version of [RFC 0002](https://docs.kuadrant.io/1.0.x/architecture/rfcs/0002-well-known-attributes/). The **Auth** and **RL** columns show availability for use within an AuthPolicy or RateLimitPolicy. Attributes deprecated in version 1.7 appear in a separate table below.

- [Request attributes](#request-attributes)
- [Connection attributes](#connection-attributes)
- [Metadata and filter state attributes](#metadata-and-filter-state-attributes)
- [Auth attributes](#auth-attributes)
- [Rate-limit attributes](#rate-limit-attributes)
- [Deprecated attributes](#deprecated-attributes)

## Request attributes

These attributes describe the HTTP request handled by the API gateway or proxy.

| Attribute | Type | Description | Auth | RL |
| --- | --- | --- | :---: | :---: |
| `request.id` | String | Request ID from the `x-request-id` header. | ✓ | ✓ |
| `request.time` | Timestamp | Time when the first request byte arrived. | ✓ | ✓ |
| `request.protocol` | String | HTTP protocol version: `HTTP/1.0`, `HTTP/1.1`, `HTTP/2`, or `HTTP/3`. | ✓ | ✓ |
| `request.scheme` | String | URL scheme, such as `http` or `https`. | ✓ | ✓ |
| `request.host` | String | Host portion of the URL. | ✓ | ✓ |
| `request.method` | String | HTTP method, such as `GET`. | ✓ | ✓ |
| `request.path` | String | Path portion of the URL. | ✓ | ✓ |
| `request.url_path` | String | URL path without the query string. |  | ✓ |
| `request.query` | String | Query string, such as `name1=value1&name2=value2`. | ✓ | ✓ |
| `request.headers` | `Map<String, String>` | Request headers keyed by lower-case header name. | ✓ | ✓ |
| `request.referer` | String | Value of the `Referer` request header. |  | ✓ |
| `request.useragent` | String | Value of the `User-Agent` request header. |  | ✓ |
| `request.size` | Number | Request size in bytes, or `-1` when the size is unknown. | ✓ |  |

## Connection attributes

These attributes describe the downstream connection to the gateway or proxy. They can apply to HTTP requests as well as connections handled at layers 3 and 4.

| Attribute | Type | Description | Auth | RL |
| --- | --- | --- | :---: | :---: |
| `source.address` | String | Remote address of the downstream connection. | ✓ | ✓ |
| `source.port` | Number | Remote port of the downstream connection. | ✓ | ✓ |
| `source.service` | String | Canonical service name of the source peer. | ✓ |  |
| `source.labels` | `Map<String, String>` | Labels associated with the source peer, such as Kubernetes pod labels or VM tags. They can come from an X.509 certificate or other configuration. | ✓ |  |
| `source.principal` | String | Authenticated source peer identity, taken from an X.509 URI SAN, DNS SAN, or Subject, in that order. The format depends on the issuer, for example a SPIFFE URI. | ✓ |  |
| `source.certificate` | String | X.509 certificate used to authenticate the source peer, provided as URL-encoded PEM. | ✓ |  |
| `destination.address` | String | Local address of the downstream connection. | ✓ | ✓ |
| `destination.port` | Number | Local port of the downstream connection. | ✓ | ✓ |
| `destination.service` | String | Canonical service name of the destination peer. | ✓ |  |
| `destination.labels` | `Map<String, String>` | Labels associated with the destination peer, such as Kubernetes pod labels or VM tags. They can come from an X.509 certificate or other configuration. | ✓ |  |
| `destination.principal` | String | Authenticated destination peer identity, taken from an X.509 URI SAN, DNS SAN, or Subject, in that order. The format depends on the issuer, for example a SPIFFE URI. | ✓ |  |
| `destination.certificate` | String | X.509 certificate used to authenticate the destination peer, provided as URL-encoded PEM. | ✓ |  |
| `connection.id` | Number | Downstream connection ID. |  | ✓ |
| `connection.mtls` | Boolean | Whether TLS is in use and the peer presented a certificate. |  | ✓ |
| `connection.requested_server_name` | String | Server name requested in the downstream TLS connection. |  | ✓ |
| `connection.tls_session.sni` | String | Server Name Indication (SNI) used for the TLS session. | ✓ |  |
| `connection.tls_version` | String | TLS version of the downstream connection. |  | ✓ |
| `connection.subject_local_certificate` | String | Subject of the local certificate in the downstream TLS connection. |  | ✓ |
| `connection.subject_peer_certificate` | String | Subject of the peer certificate in the downstream TLS connection. |  | ✓ |
| `connection.dns_san_local_certificate` | String | First DNS SAN entry in the local certificate. |  | ✓ |
| `connection.dns_san_peer_certificate` | String | First DNS SAN entry in the peer certificate. |  | ✓ |
| `connection.uri_san_local_certificate` | String | First URI SAN entry in the local certificate. |  | ✓ |
| `connection.uri_san_peer_certificate` | String | First URI SAN entry in the peer certificate. |  | ✓ |
| `connection.sha256_peer_certificate_digest` | String | SHA-256 digest of the peer certificate, when present. |  | ✓ |

## Metadata and filter state attributes

These attributes come from metadata and state recorded in the Envoy proxy filter chain.

| Attribute | Type | Description | Auth | RL |
| --- | --- | --- | :---: | :---: |
| `metadata` | Metadata | Dynamic request metadata. | ✓ | ✓ |
| `filter_state` | `Map<String, String>` | Filter-state names mapped to their serialized string values. |  | ✓ |

## Auth attributes

These attributes are available only in the external authorization service, Authorino.

| Attribute | Type | Description | Auth | RL |
| --- | --- | --- | :---: | :---: |
| `auth.identity` | Any | Identity resolved after verification. | ✓ |  |
| `auth.metadata` | `Map<String, Any>` | Metadata fetched from external sources. | ✓ |  |
| `auth.authorization` | `Map<String, Any>` | Results of authorization rules that granted access. | ✓ |  |
| `auth.response` | `Map<String, Any>` | Response objects produced after access was granted. | ✓ |  |
| `auth.callbacks` | `Map<String, Any>` | Response objects returned by callback requests. | ✓ |  |

Authorino also supports [modifiers](https://github.com/Kuadrant/authorino/blob/main/docs/features.md) in attribute paths to transform selected values.

## Rate-limit attributes

These attributes are available only in the rate-limiting service, Limitador.

| Attribute | Type | Description | Auth | RL |
| --- | --- | --- | :---: | :---: |
| `ratelimit.domain` | String | Rate-limit domain used to separate configuration by application in a multi-tenant deployment. |  | ✓ |
| `ratelimit.hits_addend` | Number | Number of hits added for a request. The value is fixed at `1` in this specification and reserved for future use. |  | ✓ |

## Deprecated attributes

The following request attributes were deprecated in version 1.7.

| Attribute | Type | Description | Auth | RL | Version |
| --- | --- | --- | :---: | :---: | --- |
| `request.body` | String | Request body. Disabled by default and requires additional proxy configuration. | ✓ |  | 1.7 |
| `request.raw_body` | `Array<Number>` | Request body as bytes. Proxy configuration determines whether this or `request.body` is available. | ✓ |  | 1.7 |
| `request.context_extensions` | `Map<String, String>` | Additional values sent to the auth service without forwarding them upstream. Requires proxy configuration. | ✓ |  | 1.7 |

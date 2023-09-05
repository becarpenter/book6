## Obsolete techniques

As IPv6 has matured and people have gained operational experience,
various co-existence and transition techniques have either been shown to
be unsatisfactory or have simply been overtaken by events. This section
simply lists such techniques, with minimal explanation. Readers are
advised to ignore these techniques for new deployments, and to consider
removing them from existing deployments.

Tunneling IPv6 over IPv4, or the converse, remains fundamental to
co-existence, although various specific tunnel mechanisms are listed
below as obsolete.

Note that three such mechanisms (6to4, Teredo and ISATAP) have left
behind them some operational security risks related to IPv4 protocol
type 41, as described in
[Plight at the End of the Tunnel - Legacy IPv6 Transition Mechanisms in the Wild](https://doi.org/10.1007/978-3-030-72582-2_23),
preprint [here](https://dataplane.org/jtk/publications/kgkp-pam-21.pdf).

- Transmission of IPv6 over IPv4 Domains without Explicit Tunnels
  \[[RFC2529](https://www.rfc-editor.org/info/rfc2529)\]. As far as is
  known, this was never deployed in practice.

- IPv6 Tunnel Broker
  \[[RFC3053](https://www.rfc-editor.org/info/rfc3053)\].

- Connection of IPv6 Domains via IPv4 Clouds ("6to4")
  \[[RFC3056](https://www.rfc-editor.org/info/rfc3056)\]
  \[[RFC3068](https://www.rfc-editor.org/info/rfc3068)\]. The problems
  with this are documented in
  [RFC6343](https://www.rfc-editor.org/info/rfc6343) and it was largely
  deprecated by [RFC7526](https://www.rfc-editor.org/info/rfc7526).

- Teredo: Tunneling IPv6 over UDP through Network Address Translations
  (NATs) \[[RFC4380](https://www.rfc-editor.org/info/rfc4380)\].

- SOCKS-based IPv6/IPv4 Gateway
  \[[RFC3089](https://www.rfc-editor.org/info/rfc3089)\].

- ISATAP \[[RFC5214](https://www.rfc-editor.org/info/rfc5214)\].

- 6rd \[[RFC5569](https://www.rfc-editor.org/info/rfc5569)\].

- An Incremental Carrier-Grade NAT (CGN) for IPv6 Transition
  \[[RFC6264](https://www.rfc-editor.org/info/rfc6264)\].

- 6a44 \[[RFC6751](https://www.rfc-editor.org/info/rfc6751)\].

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Translation%20and%20IPv4%20as%20a%20service.md) [<ins>Next</ins>](IPv6%20primary%20differences%20from%20IPv4.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

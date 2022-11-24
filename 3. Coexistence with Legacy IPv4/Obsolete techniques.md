## Obsolete techniques

As IPv6 has matured and people have gained operational experience, various co-existence and transition techniques have either been shown to be unsatisfactory or have simply been overtaken by events. This section simply lists such techniques, with minimal explanation. Readers are advised to ignore these techniques for new deployments, and to consider removing them from existing deployments.

Tunneling IPv6 over IPv4, or the converse, remains fundamental to co-existence, although various specific tunnel mechanisms are listed below. 

* Transmission of IPv6 over IPv4 Domains without Explicit Tunnels [RFC2529](https://www.rfc-editor.org/info/rfc2529). As far as is known, this was never deployed in practice.

* Connection of IPv6 Domains via IPv4 Clouds ("6to4") [RFC3056](https://www.rfc-editor.org/info/rfc3056), [RFC3068](https://www.rfc-editor.org/info/rfc3068). The problems with this are documented in [RFC6343](https://www.rfc-editor.org/info/rfc6343) and it was largely deprecated by [RFC7526](https://www.rfc-editor.org/info/rfc7526).

* 6rd [RFC5569](https://www.rfc-editor.org/info/rfc5569).

* Teredo: Tunneling IPv6 over UDP through Network Address Translations (NATs) [RFC4380](https://www.rfc-editor.org/info/rfc4380).

* TBD - more to be added here

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Translation.md) [<ins>Next</ins>](IPv6%20primary%20differences%20from%20IPv4.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)
## Routing

This section is a short introduction to a complex topic. IPv6 packets are routed individually and statelessly, like any datagram protocol. Consecutive packets may follow different routes, may be lost on the way, may arrive out of order, and transit times are variable. In practice, operators attempt to minimize these effects but upper layer protocols cannot rely on this. In some cases, quality of service mechanisms such as differentiated services \[{{2.Traffic class and flow label}}] may help, but packet delivery remains statistical.

IPv6 routing in general operates by longest-match, i.e. each router forwards each packet to another router known to handle an address prefix that is the longest one (up to 128 bits) that matches the packet's destination address \[[BCP198](https://www.rfc-editor.org/info/bcp198)]. Routers use various routing protocols among themselves to distribute information about which prefixes they handle. Common routing protocols are:

*For site and enterprise networks:*

- OSPFv3 \[[RFC5340](https://www.rfc-editor.org/info/rfc5340)] is most common.

- IS-IS \[[RFC5308](https://www.rfc-editor.org/info/rfc5308), [RFC7775](https://www.rfc-editor.org/info/rfc7775)].

- RIPng \[[RFC2080](https://www.rfc-editor.org/info/rfc2080), [RFC2081](https://www.rfc-editor.org/info/rfc2081)] is defined but seems to be little used.

*Inside carrier (ISP) networks or very large enterprise networks:*

- IBGP (internal use of BGP-4) optimized by route reflection \[[RFC4456](https://www.rfc-editor.org/info/rfc4456)].

- IS-IS \[[RFC5308](https://www.rfc-editor.org/info/rfc5308), [RFC7775](https://www.rfc-editor.org/info/rfc7775)]

- OSPFv3 \[[RFC5340](https://www.rfc-editor.org/info/rfc5340)].

*Between carrier (ISP) networks (inter-domain routing):*

- Border Gateway Protocol 4 (BGP-4) \[[RFC2545](https://www.rfc-editor.org/info/rfc2545), [RFC4271](https://www.rfc-editor.org/info/rfc4271), [RFC4760](https://www.rfc-editor.org/info/rfc4760)]. Autonomous System numbers work the same way for IPv6 and IPv4.

*For emerging mesh networks:*

- RPL (IPv6 Routing Protocol for Low-Power and Lossy Networks) \[[RFC6550](https://www.rfc-editor.org/info/rfc6550), [RFC9008](https://www.rfc-editor.org/info/rfc9008), [RFC9010](https://www.rfc-editor.org/info/rfc9010)]. 

- The Babel Routing Protocol \[[RFC8966](https://www.rfc-editor.org/info/rfc8966)].

IPv6 routers can be placed in various categories, each of which requires different features to be active:

- Customer Edge (CE) routers (enterprise): These are routers that connect an enterprise network to one or more ISPs \[[RFC7084](https://www.rfc-editor.org/info/rfc7084)].

- Enterprise routers: Internal routers within a large enterprise network.

- Subnet routers: Internal routers that support one or more links connecting end hosts (typically Ethernet or WiFi). Such a router will be the last-hop router for incoming traffic and the first-hop router for outgoing traffic. It must also provide Router Advertisement services for the end hosts, and either SLAAC or DHCPv6 or both.

- Customer Edge (CE) routers (domestic): These are cheap routers connecting home or small office networks to an ISP. They typically act as subnet routers too, but are unlikely to provide the full set of enterprise CE router services.

- Provider Edge routers. These are routers within ISP networks that directly connect to CE routers.

- Transit routers within ISPs.

- Inter-domain routers connecting ISPs to peer ISPs and/or Internet Exchange Points.


<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](DNS.md) [<ins>Next</ins>](Transport%20protocols.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)

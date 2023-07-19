## Tunnels

At its simplest, two IPv6 hosts or networks can be joined together via
IPv4 with a tunnel, i.e. an arrangement whereby a device at each end
acts as a tunnel end-point. Typically such a tunnel connects two IPv6
routers, using a very simple IPv6-in-IPv4 encapsulation described in
[RFC4213](https://www.rfc-editor.org/info/rfc4213), with IP Protocol
number 41 to tell IPv4 that the payload is IPv6. Conversely,
IPv4-in-IPv6 tunnels are also possible, with IPv6 Next Header value 4 to
tell IPv6 that the payload is IPv4. This would allow an operator to
interconnect two IPv4 islands across an IPv6 backbone. (Naturally,
IPv6-in-IPv6 tunnels are also possible, if needed.)

However, such simple encapsulation is rarely needed today, with direct
IPv6 transit being widely available from major ISPs. Tunnels are used in
other co-existence scenarios, some of which we will now describe.

Early solutions assumed that an ISP's infrastructure was primarily IPv4;
[RFC6264](https://www.rfc-editor.org/info/rfc6264) is no longer up to
date, but it provided background on how IPv6-in-IPv4 tunnels would be
used in such cases. Today, the picture is reversed, and the emphasis is
on ISP infrastructure which is primarily IPv6.

DS-Lite (Dual-Stack Lite Broadband Deployments Following IPv4
Exhaustion) \[[RFC6333](https://www.rfc-editor.org/info/rfc6333)\] uses
an IPv4-in-IPv6 tunnel between the the ISP's carrier-grade NAT (CGN) and
the customer's Customer Edge (CE) router. The customer is given a
private IPv4 prefix
\[[RFC1918](https://www.rfc-editor.org/info/rfc1918)\] and the CGN
translates IPv4 traffic to and from a public IPv4 address. Thus, the
infrastructure between the CGN and the CE router can be pure IPv6.

IPv6 can be tunneled using GRE (Generic Routing Encapsulation,
[RFC7676](https://www.rfc-editor.org/info/rfc7676)).

IPv6 can be tunneled over MPLS
\[[RFC4029](https://www.rfc-editor.org/info/rfc4029)\]; for example, see
"Connecting IPv6 Islands over IPv4 MPLS Using IPv6 Provider Edge Routers
(6PE)" \[[RFC4798](https://www.rfc-editor.org/info/rfc4798)\]. A common
solution is to connect IPv6 networks over IPv4 MPLS via IPv6 Provider
Edge routers (6PE)
\[[RFC4798](https://www.rfc-editor.org/info/rfc4798)\].
[RFC7439](https://www.rfc-editor.org/info/rfc7439) provided a gap
analysis for IPv6-only MPLS networks.
[RFC7552](https://www.rfc-editor.org/info/rfc7552) closed many of those
gaps. Interested readers can study a 125 page
[NANOG tutorial](https://pc.nanog.org/static/published/meetings/NANOG76/1993/20190612_Agahian_Demystifying_Ipv6_Over_v1.pdf).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Dual%20stack%20scenarios.md) [<ins>Next</ins>](Translation.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

## Address resolution

When an IPv6 node "A" becomes aware of the IPv6 address of another node
"B", and requires to send a packet to B, it must first determine whether
B is directly connected to one of the same links as A. If not, it will
need to send the packet to a router (see [Routing](Routing.md)). This is
known as "on-link determination". The simplest case is when the address
of B is a link local address as described in [Addresses](Addresses.md).
In that case, it is necessarily on-link. In cases where B has a
routeable address, A can determine whether it is on-link by consulting
information received from Router Advertisement (RA) messages. This
process is well described in
[RFC 4861](https://www.rfc-editor.org/info/rfc4861), so is not repeated
here.

When A has determined that B's address is on-link, and in the process
determined which interface that link is connected to, it starts address
resolution, also known as neighbor discovery (ND) or neighbor discovery
protocol (NDP). It multicasts a
Neighbor Solicitation message via that interface to the relevant link
local multicast address, which is known as the solicited-node multicast
address. This is defined in
[RFC 4291](https://www.rfc-editor.org/info/rfc4291), but explained in
[RFC 4861](https://www.rfc-editor.org/info/rfc4861). Neighbor
Solicitation is a specific form of ICMPv6 message; ICMPv6 is defined in
[RFC 8200](https://www.rfc-editor.org/info/rfc8200). Since this is a
link local multicast, such messages never escape the local link.

All IPv6 nodes **MUST** monitor multicasts sent to the solicited-node
multicast address. When B receives the Neighbor Solicitation from A, it
replies with a Neighbor Advertisement ICMPv6 message, sent unicast to
A's link local address. A will then decode that message to obtain B's
Layer 2 address (typically an IEEE MAC address), and will record the
information in its Neighbor Cache for future use. At that point, A has
all the information it needs to send packets to B.

These are the essentials of address resolution; readers who want more
detail should consult
[RFC 4861](https://www.rfc-editor.org/info/rfc4861).

This mechanism works well on a small scale, and it was designed with
full knowledge of the "ARP storms" experienced on large bridged
Ethernets running IPv4. However, it can cause significant multicast
overloads on large bridged WiFi networks, and is made worse by the need
for duplicate address detection (DAD) described in the next section.
Multicast is badly supported by large WiFi networks, as discussed in
[RFC 9119](https://www.rfc-editor.org/info/rfc9119) and in Section 4.2.1
of [RFC 5757](https://www.rfc-editor.org/info/rfc5757). As an absolute
minimum, the WiFi infrastructure switches in a large network need to
support *MLD snooping* as explained in
[RFC 4541](https://www.rfc-editor.org/info/rfc4541). "MLD" means
"Multicast Listener Discovery" and is the mechanism used by IPv6 routers
to identify which nodes require to receive packets sent to a given
multicast address. Version 2 of MLD is specified by
[RFC 3810](https://www.rfc-editor.org/info/rfc3810). Of course, all IPv6
nodes must join the `ff02::1` multicast group, as well as the relevant
solicited-node multicast group, so MLD snooping does not avoid the
scaling problem, but at least it suppresses multicasts on WiFi segments
that do not need them.

Some optimizations have been defined, such as Gratuitous Neighbor
Discovery \[[RFC9131](https://www.rfc-editor.org/info/rfc9131)\], but
further standards work is needed in this area.

Operational issues with neighbor discovery and wireless multicast have
been analyzed in the past
([RFC 6583](https://www.rfc-editor.org/info/rfc6583),
[RFC 6636](https://www.rfc-editor.org/info/rfc6636),
[RFC 9119](https://www.rfc-editor.org/info/rfc9119)), but it remains the
case that very large WiFi networks (such as the IETF builds several
times a year for its plenary meetings) are subject to significant
multicast overloads. In practice, this causes the WiFi switches to
arbitrarily throttle the rate of multicasting, so neighbor discovery
proceeds very slowly. It is **strongly** recommended to limit the size
of wireless subnets as much as practicable.

A summary of the issues and complications of neighbor discovery on
wireless networks in general (not just WiFi) can be found in
[this draft](https://datatracker.ietf.org/doc/draft-ietf-6man-ipv6-over-wireless/).

Considerable work has been done to alleviate these problems in the case
of Low-Power Wireless Personal Area Networks (6LoWPANs, using the IEEE
802.15.4 standard). Relevant RFCs include
[RFC 6775](https://www.rfc-editor.org/info/rfc6775),
[RFC 8505](https://www.rfc-editor.org/info/rfc8505),
[RFC 8928](https://www.rfc-editor.org/info/rfc8928),
[RFC 8929](https://www.rfc-editor.org/info/rfc8929) and
[RFC9685](https://www.rfc-editor.org/info/rfc9685). These improvements
might be applied more generally in future.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Layer%202%20functions.md) [<ins>Next</ins>](Auto-configuration.md) [<ins>Top</ins>](02.%20IPv6%20Basic%20Technology.md)

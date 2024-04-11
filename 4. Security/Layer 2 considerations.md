## Layer 2 considerations

IPv6 is comparatively flexible at the link layer. Flexibility typically
comes with complexity, which can drive security challenges.

Initially, there was a belief that cryptographic SEcure Neighbor
Discovery (SEND, [RFC3971](https://www.rfc-editor.org/info/rfc3971))
would resolve the majority of neighbor discovery risks. Unfortunately,
SEND was not accepted by the market. Hence, the security problems
discussed in [RFC3756](https://www.rfc-editor.org/info/rfc3756) section
4.1 are still active:

- A malicious node could answer to Duplicate Address Discovery (DAD) for
  any request of a legitimate node, amounting to a denial of service
  attack;
- A malicious node could poison the neighbor cache of another node
  (especially the router) to intercept traffic directed to another node
  (man-in-the-middle attack); it is possible for neighbor solicitation
  and neighbor advertisement in many different cases.

There is no big difference here from IPv4 ARP spoofing. Of course, the
danger only exists if a bad actor succeeds in implanting a malicious
node. Where this is felt to be a significant risk, the strongest
protection method is host isolation on a separate link with a separate
dedicated /64 prefix. IPv6 has enough address space to follow this
strategy. All subscribers (including mobile) already have at least one
/64 prefix. A /56 prefix is considered as the minimum for ordinary
domestic subscribers with the possibility for /48 for even a small
business. The latter would theoretically allow 65,535 hosts each to have
their own /64.

An alternative method of protection is Source Address Validation
Improvement (SAVI) - see
[RFC6620](https://www.rfc-editor.org/info/rfc6620) which is based on
the full Neighbor Discovery (ND) exchange monitoring by the switch to
dynamically install filters. Like SEND, it is not a very popular
solution.

Cellular mobile links (3GPP etc.) are always a point-to-point tunnel.
Hence, it was possible to greatly simplify the ND protocol (address
resolution and DAD are unnecessary) to avoid complexity and the majority
of security threats – see
[RFC7849](https://www.rfc-editor.org/info/rfc7849).

It is of the same importance as for IPv4 to restrict who could claim the
default router and DHCP server functionality because it is the best way
to organize man-in-the-middle attacks. Hence, RA-Guard
[RFC6105](https://www.rfc-editor.org/info/rfc6105) and DHCPv6-Shield
[RFC7610](https://www.rfc-editor.org/info/rfc7610) are defined.
Unfortunately, there is a possibility to hide the purpose of a packet by
prepending the transport layer with extension headers (especially
dangerous fragmentation). Hence,
[RFC7113](https://www.rfc-editor.org/info/rfc7113) and
[RFC7112](https://www.rfc-editor.org/info/rfc7112) are additionally
needed for protection against rogue Router or DHCP.

There is a new security attack vector related to IPv6 specifically.
SLAAC address acquisition is distributed, so the router may not know all
addresses configured on the link even if all ND exchange is monitored by
the router. Hence, the router needs to request address resolution after
the first packet of a new session is received from an external source.
At the same time, the IPv6 link address space is huge (2^64) by default.
Hence, it is potentially possible to force the router (even from an
external network) for address resolution a huge number of times. It is
an effective DoS attack that has simple protection measures.
[RFC6583](https://www.rfc-editor.org/info/rfc6583) discusses how to
rate-limit the number of address resolution requests or minimize subnet
size.

ND heavily relies on multicast which may create problems in the wireless
environment. See
[2. Address resolution](../2.%20IPv6%20Basic%20Technology/Address%20resolution.md)
and
[Multicast efficiency](https://datatracker.ietf.org/doc/draft-vyncke-6man-mcast-not-efficient).
ND DoS activity may be effective for that reason but the attacker should
be local to the link. Hence, perimeter security may help. The multicast
storm is less of a problem in a wireline environment because of MLD
snooping typically implemented on the link
([RFC4541](https://www.rfc-editor.org/info/rfc4541)).

IPv6 has a new feature that improves privacy. It is normal for an IPv6
host to have many IP addresses for the same interface, often with
unpredictable (pseudo-random) IID values. Some IP addresses may be used
temporarily ([RFC8981](https://www.rfc-editor.org/info/rfc8981)) which
creates a challenge for intermediate Internet nodes to trace suspicious
user activity, for the same reason that it protects privacy.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Filtering.md) [<ins>Chapter Contents</ins>](4.%20Security.md)

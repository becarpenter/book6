## Layer 2 considerations

IPv6 is much more flexible at the link layer. Flexibility typically comes with complexity. Complexity is driving security challenges.

Initially, there was a belief that cryptography [RFC 3971](https://www.rfc-editor.org/info/rfc3971) would resolve the majority of link problems. Unfortunately, SEND was not accepted by the market.
Hence, the security problems discussed in [RFC 3756](https://www.rfc-editor.org/info/rfc3756) section 4.1 are still not resolved: 
-	A malicious node could answer DAD for any request of a legitimate node (denial of service attack);
-	A malicious node could poison the cache of another node (especially the router) to intercept traffic directed to another node (man-in-the-middle attack); it is possible for neighbor solicitation and neighbor advertisement in many different cases.
There is no big difference here from IPv4 ARP spoofing.
The strongest protection method is host isolation in the separate link with the separate /64 prefix. IPv6 has enough address space to follow this strategy, all subscribers (including Mobile) already have at least /64 prefixes, /56 is considered as a minimum for ordinary subscribers with the possibility for /48 for a small business.
An alternative method of protection is SAVI - see [RFC 6620](https://www.rfc-editor.org/info/rfc6620) which is based on the full ND exchange monitoring by the switch to dynamically install filters. It is not a very popular solution.

Mobile link is always a P2P tunnel. Hence, it was possible to greatly simplify ND protocol (address resolution and DAD are canceled) to avoid complexity and the majority of security threats – see [RFC 7849](https://www.rfc-editor.org/info/rfc7849). 

It is of the same importance as for IPv4 to restrict who could claim the default router and DHCP server functionality because it is the best way to organize man-in-the-middle attacks. Hence, RA-Guard [RFC 6105](https://www.rfc-editor.org/info/rfc6105) and DHCPv6-Shield [RFC 7610](https://www.rfc-editor.org/info/rfc7610) are expected. Unfortunately, there is a possibility to hide the packet purpose by prepending the transport layer with extension headers (especially dangerous fragmentation). Hence, [RFC 7113](https://www.rfc-editor.org/info/rfc7113) and [RFC 7112](https://www.rfc-editor.org/info/rfc7112) are additionally needed for protection against rogue Router or DHCP.

There is a new security attack vector related to IPv6 specifically. SLAAC address acquisition is distributed, the router may not know all addresses appointed on the link even if all ND exchange is monitored by the router. Hence, the router needs to request address resolution after a new session packet is received.
At the same time, the IPv6 link address space is huge (2^64) by default. Hence, it is potentially possible to enforce the router (even from an external network) for address resolution a huge number of times. It is an effective DoS attack that has simple protection measures. [RFC 6583](https://www.rfc-editor.org/info/rfc6583) discusses how to rate-limit the number of address resolution requests or minimize subnet size.

ND heavily relies on multicast which may create problems in the wireless environment [Multicast efficiency]( https://datatracker.ietf.org/doc/html/draft-vyncke-6man-mcast-not-efficient-01). ND DoS activity may be effective for that reason but the attacker should be local to the link. Hence, perimeter security may help.
The multicast storm is less of a problem in a wireline environment because of MLD snooping typically implemented on the link [RFC 4541](https://www.rfc-editor.org/info/rfc4541).

IPv6 has a new feature that improves privacy. It is normal for an IPv6 host to have many IP addresses for the same interface. Some IP addresses may be used temporarily [RFC 8981](https://www.rfc-editor.org/info/rfc8981) which creates a challenge for intermediate Internet nodes to trace user activity.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Next</ins>](Filtering%20.md) [<ins>Chapter Contents</ins>](4.%20Security.md)

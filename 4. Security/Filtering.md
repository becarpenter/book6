## Filtering

Filtering is a big part of internet operation.
IPv6 filtering in general may be easy because of the hierarchical address plan.
But the one filter almost always consumes 4x more resources in products. Hence, it may affect scalability or performance.

The majority of practices do not change with IPv6 adoption:
-	[BCP 38](https://www.rfc-editor.org/info/rfc2827) instructs carriers to filter addresses on ingress to prevent address spoofing, addresses should be from the range delegated to this client.
-	Martian addresses should be filtered on the perimeter according to [RFC 6890](https://www.rfc-editor.org/info/rfc6890). Just in the case of IPv6, it refers [IANA IPv6 Special-Purpose Address Registry](https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml).
-	Filtering on [BGP Peering](https://www.rfc-editor.org/info/rfc7454) and [RPKI](https://www.rfc-editor.org/info/rfc8210) have no change for IPv6.
-	The router’s control plane protection [RFC 6192](https://www.rfc-editor.org/info/rfc6192) is universal for IPv6 or IPv4.
-	[Remote Triggered Black Hole](https://www.rfc-editor.org/info/rfc5635) is the same for IPv4 and IPv6, just the prefix for IPv6 [100::/64](https://www.rfc-editor.org/info/rfc6666) has been defined separately.
-	All IGP protocols should filter announcements for the local link according to [RFC 5082](https://www.rfc-editor.org/info/rfc5082). In the case of IPv6, it means that announcements are allowed only from LLA addresses.
-	[DNSSEC](https://www.rfc-editor.org/info/rfc4641) is the same recommended independent of A or AAAA requests.

Some filters are specific to IPv6.

The biggest difference is related to the huge subnet size (/64), filtering on the long prefix is useless, especially with dynamic temporary addresses that the host may generate. Moreover, if there is a desire to filter one subscriber it may need to filter even shorter prefixes. It is recommended to filter /64 initially and then monitors the situation, if the problem would persist then filter /60, then /56. /48 is the maximum that may belong to the ordinary subscriber, it does not make sense to filter shorter prefixes to cover a subscriber.
The address plan design of the organization may be different, including /128 addresses with DHCP acquisition but it is never possible to understand it from the outside. If the organization employs SLAAC then again /64 is the minimum that makes sense to filter.

The addresses of different scopes should be filtered at respective borders:
-	LLA should be not forwarded outside of the link according to [IPv6 Addressing Architecture](https://www.rfc-editor.org/info/rfc4291),
-	ULA should be filtered at organization borders according to [RFC 4193](https://www.rfc-editor.org/info/rfc4193),
-	Multicast addresses have 5 defined scopes (Interface, Link, Admin, Site, and Organization) according to [IPv6 Addressing Architecture](https://www.rfc-editor.org/info/rfc4291) that should be filtered at respective borders. For the lowest scopes, the perimeter is evident and typically hard-coded into nodes. For the scopes with flexible borders (like Admin, Site, Organization) it needs a special configuration.

PMTUD operation is more important in IPv6 because fragmentation is prohibited in transit. Hence, ICMP filtering may do more harm in IPv6. It is discussed in [Recommendations for ICMPv6 filtering](https://www.rfc-editor.org/info/rfc4890) what should be dropped or permitted.

Security devices and destination nodes should check that the first fragment should have all headers (including the transport layer) and fragments should not have an overlap according to [RFC 8200](https://www.rfc-editor.org/info/rfc8200).

[Filtering recommendations for packets with extension headers](https://www.rfc-editor.org/info/rfc9288) is oriented for the transit case where filtering now is excessive. It motivates what particular EHs to permit, drop, reject (with ICMP), rate-limit, or ignore. It is important to mention that these additional actions are recommended in addition to the basic rule of [RFC 7045](https://www.rfc-editor.org/info/rfc7045) to allow by default the transmission of all extension headers in transit.

Filtering ND messages on the link is discussed in [<ins>Address resolution<ins>](../4.%20Security/Layer%202%20considerations.md).

There is a big danger for IPv4-only networks because IPv6 is preferred on hosts. Hence, the activation of IPv6 by the malicious node may create many security problems. [Security Implications of IPv6 on IPv4 Networks](https://www.rfc-editor.org/info/rfc7123) discusses what is important to block in this scenario. These are primarily different tunneling protocols that may help to bypass perimeter security and rogue DHCP or Router for a man-in-the-middle attack.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Layer%202%20considerations.md) [<ins>Chapter Contents</ins>](4.%20Security.md)

## Filtering

Filtering is a big part of safe Internet connection. IPv6 filtering in
general may be easy because of the hierarchical address plan. However,
each filter almost always consumes four times more resources in
products. This may affect scalability or performance, if equipment is
underprovisioned.

The majority of practices do not change with IPv6 adoption:

- [BCP 38](https://www.rfc-editor.org/info/bcp38) recommends carriers to
  filter traffic based on *source* addresses on ingress from the client
  to prevent address spoofing. Source addresses in the range delegated
  to this client are allowed; other sources addresses should be filtered
  (except for the case mentioned in
  \[[6. Multi-prefix operation](../6.%20Management%20and%20Operations/Multi-prefix%20operation.md)\]).
  Operators that do not implement BCP38 are condoning address spoofing.
- "Martian" addresses should be filtered on the perimeter according to
  [RFC 6890](https://www.rfc-editor.org/info/rfc6890). In the case of
  IPv6, this refers to the
  [IANA IPv6 Special-Purpose Address Registry](https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml).
- Filtering on [BGP Peering](https://www.rfc-editor.org/info/rfc7454)
  and [RPKI](https://www.rfc-editor.org/info/rfc8210) do not change for
  IPv6.
- The router’s control plane protection
  \[[RFC6192](https://www.rfc-editor.org/info/rfc6192)\] is universal
  for IPv6 or IPv4.
- [Remote Triggered Black Hole](https://www.rfc-editor.org/info/rfc5635)
  is the same for IPv4 and IPv6, except that the prefix for IPv6
  [100::/64](https://www.rfc-editor.org/info/rfc6666) has been defined
  separately.
- All IGP protocols should filter announcements for the local link
  according to [RFC 5082](https://www.rfc-editor.org/info/rfc5082). In
  the case of IPv6, this means that announcements are allowed only from
  link-local addresses.
- [DNSSEC](https://www.rfc-editor.org/info/rfc4641) is recommended,
  independent of A or AAAA requests.

Some filters are specific to IPv6.

The biggest difference is related to the typical prefix size (/64).
Filtering anything longer than this is useless, because of the
unpredictable temporary addresses that a host may generate. Moreover, if
there is a desire to filter one subscriber it may be apprpriate to
filter even shorter prefixes, such as a /56. It is recommended to filter
/64 initially and then monitor the situation; if the problem persists,
then filter /60, then /56. /48 is the maximum that may belong to an
ordinary subscriber, so it does not make sense to filter shorter prefixes
than that to block a single subscriber.

The address plan design of an organization may be different, including
/128 addresses with DHCPv6 configuration, but it is never possible to
know this from the outside. If the organization employs SLAAC then again
/64 is the minimum that makes sense to filter.

The addresses of different scopes should be filtered at respective
borders:

- LLA should be not forwarded outside of the link according to
  [IPv6 Addressing Architecture](https://www.rfc-editor.org/info/rfc4291),
- ULA should be filtered at organization borders according to
  [RFC 4193](https://www.rfc-editor.org/info/rfc4193),
- Multicast addresses have 5 defined scopes (Interface, Link, Admin,
  Site, and Organization) according to
  [IPv6 Addressing Architecture](https://www.rfc-editor.org/info/rfc4291)
  that should be filtered at respective borders. For the lowest scopes,
  the perimeter is evident and typically hard-coded into nodes. For the
  scopes with flexible borders (like Admin, Site, Organization) it needs
  a special configuration.

PMTUD operation is more important in IPv6 because fragmentation is
prohibited in transit. Hence, ICMP filtering may do more harm in IPv6.
It is discussed in
[Recommendations for ICMPv6 filtering](https://www.rfc-editor.org/info/rfc4890)
what should be dropped or permitted.

Security devices and destination nodes should check that the first
fragment should have all headers (including the transport layer) and
fragments should not have an overlap according to
[RFC 8200](https://www.rfc-editor.org/info/rfc8200).

[Filtering recommendations for packets with extension headers](https://www.rfc-editor.org/info/rfc9288)
is oriented for the transit case where excessive filtering is common.
This RFC motivates what particular EHs to permit, drop, reject (with
ICMP), rate-limit, or ignore. It is important to mention that these
additional actions are recommended in addition to the basic rule of
[RFC 7045](https://www.rfc-editor.org/info/rfc7045) to allow by default
the transmission of all extension headers in transit.

Limiting ND messages on the link is discussed in
[<ins>Address resolution<ins>](../2.%20IPv6%20Basic%20Technology/Address%20resolution.md).

There is a risk for IPv4-only networks caused by IPv6 preference
programmed into hosts. The activation of IPv6 by a malicious node could
create security problems.
[Security Implications of IPv6 on IPv4 Networks](https://www.rfc-editor.org/info/rfc7123)
discusses what is important to block in this scenario. These are
primarily different tunneling protocols that might help to bypass
perimeter security, and rogue DHCP or Router code for a
man-in-the-middle attack.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Layer%202%20considerations.md) [<ins>Next</ins>](Topology%20obfuscation.md) [<ins>Chapter Contents</ins>](4.%20Security.md)

## Managed configuration

Host addresses and other IPv6 parameters can be configured using the
Dynamic Host Configuration Protocol for IPv6 (DHCPv6). The players in
DHCPv6 are the client (the host to be configured), the server (providing
configuration data), and optionally DHCPv6 relay agents connecting a
host indirectly to the main server.

People sometimes wonder why both this and SLAAC exist. The reason is
partly historical (DHCP for IPv4 was new and not widely deployed when
IPv6 was designed). In addition, the concept of SLAAC (previous section)
was intended to avoid any need for a separate configuration protocol in
simple networks. The result is that even in a complicated network,
Neighbor Discovery and Router Advertisement messages remain necessary,
even if DHCPv6 is deployed.

The Android operating system does not support DHCPv6. This means that a
network that requires to support Android hosts must provide SLAAC as
well as DHCPv6. In an enterprise environment, that might lead an
operator to run a separate (WiFi) network that supports SLAAC, isolated
from other corporate networks managed using DHCPv6. Alternatively, they
may simply not provide IPv6 support for Android users. Cellular mobile
service providers do support SLAAC over a point-to-point 3GPP link from
the network to the mobile device. Public networks as in coffee-shops and
hotels, if they support IPv6 at all, do so via SLAAC. So the domain of
applicability for DHCPv6 is mainly enterprise networks. They tend to
prefer managed addresses because of security compliance requirements.

DHCPv6 is defined by
[RFC 8415](https://www.rfc-editor.org/info/rfc8415). It is conceptually
similar to DHCP for IPv4, but different in detail. When it is in use,
each host must contain a DHCPv6 client and either a DHCPv6 server or a
DHCPv6 relay must be available on the subnet. DHCPv6 can provide
assigned IPv6 addresses and other parameters, and new options can be
defined. (All registered DHCP parameters can be found on the
[IANA site](https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml#dhcpv6-parameters-2).)
DHCPv6 messages are transmitted over UDP/IPv6 using ports 546 and 547.

A notable feature of DHCPv6 is that it can be used *between routers* to
assign prefixes dynamically. For example, if a new segment is switched
on and its router doesn't have an IPv6 prefix, an infrastructure router
"above" it in the topology can assign it one (e.g. a /64 prefix), using
the `OPTION_IA_PD` and `OPTION_IAPREFIX` DHCPv6 options (previously
defined by RFC3633, but now covered by
[Section 6.3 of RFC8415](https://www.rfc-editor.org/rfc/rfc8415.html#section-6.3).
This process is known as DHCPv6-PD (for "prefix delegation"). Further,
it is possible to signal the availability of DHCPv6-PD in SLAAC Router
Advertisements \[[RFC9762](https://www.rfc-editor.org/info/rfc9762)\],
which allows client devices in large broadcast networks to benefit from
an IPv6 prefix per device
\[[RFC9663](https://www.rfc-editor.org/info/rfc9663)\],
\[[5. Prefix per Host](../05.%20Network%20Design/Prefix%20per%20Host.md)\].

However, the 3GPP specifications for IPv6 usage over cellular mobile
systems make both DHCPv6 and DHCPv6-PD optional
\[[RFC7066](https://www.rfc-editor.org/info/rfc7066)\], and experience
shows that many common 3GPP implementations do not support them. Thus
mobile devices can only rely on RA-based address and prefix mechanisms.

DHCPv6 message types include:

- SOLICIT (discover DHCPv6 servers)
- ADVERTISE (response to SOLICIT)
- REQUEST (client request for configuration data)
- REPLY (server sends configuration data)
- RELEASE (client releases resources)
- RECONFIGURE (server changes configuration data)

DHCPv6 options include:

- Client Identifier Option
- Server Identifier Option
- Identity Association for Non-temporary Addresses Option
- Identity Association for Temporary Addresses Option
- IA Address Option
- Authentication Option
- Server Unicast Option
- Status Code Option
- DNS Recursive Name Server Option
- Domain Search List Option
- Identity Association for Prefix Delegation Option
- IA Prefix Option

Readers who want more details should consult
[RFC 8415](https://www.rfc-editor.org/info/rfc8415) directly. Be warned,
this is a very complex RFC of about 150 pages. Also, the full lists of
defined messages and options may be found at
[IANA](https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml),
with citations of the relevant RFCs.

A missing DHCPv6 option is information about default routers; this is
only available via RAs, as described in the previous sections. No
consensus has been reached in the IETF to also supply this information
via DHCPv6. In fact, DHCPv6 is designed to supplement router
advertisement information and is not intended to work on a subnet that
has no router. Therefore DHCPv6 assigned addresses effectively have
prefix length /128, and clients need to combine that information with RA
information to communicate with other on-link hosts.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Auto-configuration.md) [<ins>Next</ins>](DNS.md) [<ins>Top</ins>](02.%20IPv6%20Basic%20Technology.md)

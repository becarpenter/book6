## Managed configuration

Host addresses and other IPv6 parameters can be configured using the Dynamic Host Configuration Protocol for IPv6 (DHCPv6). People sometimes wonder why both this and SLAAC exist. The reason is partly historical (DHCP for IPv4 was new and not widely deployed when IPv6 was designed). In addition, the concept of SLAAC (previous section) was intended to avoid any need for a separate configuration protocol in simple networks. The result is that even in a complicated network, Neighbor Discovery and Router Advertisement messages remain necessary, even if DHCPv6 is deployed.

The Android operating system does not support DHCPv6. This means that a network that requires to support Android hosts must provide SLAAC as well as DHCPv6. In an enterprise environment, that might lead an operator to run a separate (WiFi) network that supports SLAAC, isolated from the normal corporate networks managed using DHCPv6. Alternatively, they may simply not provide IPv6 support for Android users. Cellular mobile service providers do support SLAAC over a point-to-point 3GPP link from the network to the mobile device. Public networks as in coffee-shops and hotels, if they support IPv6 at all, do so via SLAAC. So the domain of applicability for DHCPv6 is mainly enterprise networks. They tend to prefer managed addresses because of security compliance requirements.

DHCPv6 is defined by [RFC8415](https://www.rfc-editor.org/info/rfc8415). It is conceptually similar to DHCP for IPv4, but different in detail. When it is in use, each host must contain a DHCPv6 client and either a DHCPv6 server or a DHCPv6 relay must be available on the subnet. DHCPv6 can provide assigned IPv6 addresses and other parameters, and new options can be defined. (All registered DHCP parameters can be found on the [IANA site](https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml#dhcpv6-parameters-2).)

A notable feature of DHCPv6 is that it can be used *between routers* to assign prefixes dynamically. For example, if a new segment is switched on and its router doesn't have an IPv6 prefix, an infrastructure router somewhere "above" it in the topology can assign it one (e.g. a /64 prefix), using the `OPTION_IA_PD` and `OPTION_IAPREFIX` DHCPv6 options (previously defined by RFC3633, but now covered by [Section 6.3 of RFC8415](https://www.rfc-editor.org/rfc/rfc8415.html#section-6.3).

DHCPv6 message types include:

- SOLICIT (discover DHCPv6 servers)
- ADVERTISE (response to SOLICIT)
- REQUEST (client request for configuration data)
- REPLY   (server sends configuration data)
- RELEASE (client releases resources)
- RECONFIGURE (server changes configuration data)

Important DHCPv6 options include:

- Client Identifier Option
- Server Identifier Option
- Identity Association for Non-temporary Addresses Option
- Identity Association for Temporary Addresses Option
- IA Address Option
- Authentication Option
- Server Unicast Option
- Status Code Option
- Identity Association for Prefix Delegation Option
- IA Prefix Option

Readers who want more details should consult [RFC8415](https://www.rfc-editor.org/info/rfc8415) directly.

A missing option is DNS server information; this is only available
via RAs, as mentioned in the previous section. No consensus has
been reached in the IETF to also supply this information via DHCPv6.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Auto-configuration.md) [<ins>Next</ins>](DNS.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)

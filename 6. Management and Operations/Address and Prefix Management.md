## Address and Prefix Management

Three main cases can be distinguished:

1. Unmanaged networks will generally use stateless address
   autoconfiguration (SLAAC,
   [RFC4862](https://www.rfc-editor.org/info/rfc4862)) within the subnet
   prefix(es) assigned to them by a service provider. This is in
   contrast to IPv4 practice, where DHCP is automatically configured in
   most unmanaged networks.

1. Provider networks will generally configure prefixes and addresses on
   network elements, including customer gateways, according to a
   predefined plan as discussed in
   \[[5. Address Planning](../5.%20Network%20Design/Address%20Planning.md)\].
   DHCPv6 Prefix Delegation `OPTION_IA_PD` may be used to assign
   prefixes to routers, even if DHCPv6 is not used for address
   assignment
   \[[2. Managed configuration](../2.%20IPv6%20Basic%20Technology/Managed%20configuration.md)\].

1. Managed enterprise networks will prepare an addressing and subnet
   plan that meets their specific requirements. To take a very simple
   example, an enterprise given a /48 prefix by its ISP might assign a
   /56 to each branch office and then assign /64 subnets as needed
   within each branch. The decision must then be taken whether to deploy
   SLAAC throughout the network, or to use DHCPv6 `OPTION_IA_NA`for
   address assignment
   \[[2. Managed configuration](../2.%20IPv6%20Basic%20Technology/Managed%20configuration.md)\].
   This choice has implications for both trouble-shooting and security
   incident management.

When a help-desk call or a security alert concerns a specific IPv6
address, the responder needs to know which computer and which user are
involved. In some security cases, this may have financial implications
and may need to meet a forensic evidentiary standard. Therefore,
ascertaining the correspondence between the address, the device, and the
user is a hard requirement for many enterprises.

In the case of SLAAC, the correspondence between IPv6 addresses and the
MAC addresses of connected devices is embedded in the neighbor discovery
caches of other devices on the same link, including the subnet router.
This is volatile information, especially if IPv6 temporary addresses
\[[RFC8981](https://www.rfc-editor.org/info/rfc8981)\] or variable MAC
addresses
\[[draft-ietf-madinas-mac-address-randomization](https://datatracker.ietf.org/doc/draft-ietf-madinas-mac-address-randomization/)\]
are in use. A supplementary mechanism is needed to extract and log this
information at a suitable frequency. An alternative would be to
continuously monitor neighbor discovery traffic and extract and log the
same information. It has also been observed that monitoring DAD
(duplicate address detection) traffic will work, as described in
[this blog](https://weberblog.net/monitoring-mac-ipv6-address-bindings/).
All these solutions have unpleasant scaling properties for a large
enterprise.

In the case of DHCPv6, the IPv6-MAC address correspondence is embedded
in the DHCP server configuration. In the simplest approach, MAC
addresses are pre-registered and neither temporary IPv6 addresses nor
variable MAC addresses are supported. However, this exposes the network
to attack, since it is trivial to forge a MAC address with most modern
equipment.

With either SLAAC or DHCPv6, the user of an unknown MAC addresses can be
authenticated by IEEE 802.1X access control, and this would provide a
robust link between the MAC address in use and the human user whose
credentials were used for authentication.

An additional factor is that one widely used host operating system,
Android, does not currently support host address assignment via DHCPv6.
One solution to this, for a dual stack deployment, is to accept that
affected devices will only use IPv4. Another is to have a separate WiFi
BSS for "bring your own" devices (BYOD) where SLAAC is available, but
this network will be treated as suspect and will be effectively outside
the corporate firewall. A third solution is to offer no service at all
for such devices, which will have to connect to a public cellular system
instead.

A network operator must make a conscious choice between SLAAC and
DHCPv6, in conjunction with their choice of IPAM (IP Address Management)
solution if applicable. An important question is whether tools exist to
meet the help desk and security needs described above _for the specific
vendor equipment and software in use_.

This book does not recommend specific products. However, it is to be
noted that an [open source solution](https://www.isc.org/kea/) does
exist that supports DHCPv6-based address management including dynamic
DNS.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Remote%20configuration.md) [<ins>Chapter Contents</ins>](6.%20Management%20and%20Operations.md)

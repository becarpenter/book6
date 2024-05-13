## Layer 2 functions

Every IPv6 packet has to be wrapped in a Layer 2 packet (or frame) for
physical transmission on the "wire", which of course is more likely to
be an optical fibre or a radio link in many cases. This statement needs
two immediate qualifications:

1. For hardware media with very small frame sizes, an IPv6 packet may
   need to be split between several Layer 2 packets. This is *not*
   fragmementation as far as IPv6 is concerned, because it is handled as
   a Layer 2 function (sometimes called an "adaptation layer"), whether
   hardware or software.

1. For IPv6-in-IPv4 tunnels, it is IPv4 that serves as Layer 2; see
   [3. Tunnels](../3.%20Coexistence%20with%20Legacy%20IPv4/Tunnels.md).

There is a considerable difference between the mapping of IPv6 onto
Ethernet-like links (including WiFi) and the mapping onto various forms
of wireless mesh networks. An Ethernet-like link (including many
point-to-point links) is one that send or receives one complete frame at
a time with a raw size of at least 1500 bytes and a 48 bit IEEE MAC
address at Layer 2. It must provide or emulate classical Ethernet
multicasting. The IPv6 mapping then follows
[RFC 2464](https://www.rfc-editor.org/info/rfc2464) from 1998, except for
some updates to multicast address details in
[RFC 6085](https://www.rfc-editor.org/info/rfc6085) and to the interface
identifier in [RFC 8064](https://www.rfc-editor.org/info/rfc8064). IPv6
has its own Ethertype field (0x86dd), so that IPv6 and IPv4 packets can
be distinguished at driver level. Documents similar to RFC 2464 exist
for several other hardware media and are often known as "IPv6-over-foo"
documents.

Interestingly, there is *no* IPv6-over-WiFi document; IPv6 relies on
WiFi completely emulating Ethernet, including multicast. This has
consequences for the scaleability of IPv6 over WiFi which are discussed
in [RFC 9119](https://www.rfc-editor.org/info/rfc9119).

A consequence of the Ethernet legacy frame size of 1500 bytes is that
the Internet-wide required minimum transmission unit size (MTU) for IPv6
is set at **1280 bytes** (reduced from 1500 to allow for possible
encapsulation overhead). Therefore, *any* IPv6-over-foo mechanism
**MUST** provide at least this MTU, and this applies to every adaptation
layer.

IPv6 can be transmitted over PPP (Point-to-Point Protocol) links
\[[RFC5072](https://www.rfc-editor.org/info/rfc5072),
[RFC 5172](https://www.rfc-editor.org/info/rfc5172)\]. Similarly, it can
be transmitted using GRE (Generic Routing Encapsulation,
[RFC 7676](https://www.rfc-editor.org/info/rfc7676)).

IPv6 can also be transmitted over MPLS infrastructure
\[[RFC4029](https://www.rfc-editor.org/info/rfc4029)\]. Further details
can be found in
\[[3. Tunnels](../3.%20Coexistence%20with%20Legacy%20IPv4/Tunnels.md)\].

Mapping IPv6 to mesh networks, which have no native support for
multicast and no simple model of a shared link like Ethernet, is rather
different. [RFC 9119](https://www.rfc-editor.org/info/rfc9119) is
relevant here too, and
[RFC 8376](https://www.rfc-editor.org/info/rfc8376) provides general
background on the challenges involved. Operational experience is limited
today and best practices are not yet established.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Addresses.md) [<ins>Next</ins>](Address%20resolution.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)

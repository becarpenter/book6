## IPv6 primary differences from IPv4

This book intentionally describes IPv6 as the "new normal" IP protocol,
but this section mentions the main ways that it differs from IPv4, using
terminology from
[2. IPv6 Basic Technology](../02.%20IPv6%20Basic%20Technology).

IPv6 is very similar for transit routing, but has some considerable
differences on the first hop for hosts as well as for routers that do
more than pure routing.

The primary differences are:

- The first difference is desirable and expected: IPv6 has a four times
  bigger address size (128 bits against 32 bits).

  SLAAC is more used on IPv6 than DHCPv6. A SLAAC subnet prefix is 64
  bits for historical reasons that are fixed in many standards. 2^64
  hosts are of course not possible in one subnet, but the address space
  is reserved even for a smartphone. Hence, it is disputable what is the
  effective IPv6 address space. It is bigger than 2^64 bits but the 64
  IID bits are utilized for privacy and security, not for addressing
  *per se*.

- NAT44 is a common solution in IPv4 networking.

  NAT66 is discouraged by IETF and not specified as a standard. IPv6
  end-to-end connectivity is considered a big value.

- IPv4 has only one address per interface (without special hacks).

  Many IPv6 addresses on every interface are the norm. It is not just
  different address types (LLA, ULA, and GUA) but additionally many
  instances of GUA and ULA for security or virtualization reasons. The
  popular ChromOS has seven IPv6 addresses as the minimum. Additionally,
  the number of IPv6 addresses per interface could almost double in the
  case of link renumbering.

- IPv4 has only centralized DHCPv4 address acquisition.

  IPv6 has additionally distributed address acquisition by SLAAC which
  is widely adopted. SLAAC considerably changes the logic of the link
  operation. (The problems caused by broadcast IPv4 ARP are replaced by
  the problems caused by multicast IPv6 Neighbor Solicitation!)

- IPv4 has a complex (many fields) and theoretically variable header
  that is practically fixed because options are not widely used.

  IPv6 has a simple and fixed header. Additionally, IPv6 could have
  extension headers that permit unlimited protocol extensibility at the
  data plane. Many extension headers are already used in limited
  domains. Just like IPv4 options, deployment of new IPv6 extensions
  headers and options across the open Internet is problematic.

- IPv4 fragmentation is in the basic header and permitted in transit.

  IPv6 fragmentation uses an extension header and is prohibited in
  transit.

- IPv4 address resolution on the link by ARP protocol is at layer 2 (for
  the IEEE 802 media it is an IEEE 802 frame). IPv6 address resolution
  on the link by ND protocol is at layer 3 (IPv6 packet over LLA or
  other IP addresses).

- Multicast is not needed for IPv4 itself.

  Multicast is mandatory for the IPv6 link operation. Many ND functions
  are using multicast. That may create advantages (for Ethernet) and
  disadvantages (for many types of wireless).

The list above is not comprehensive, but the other differences are
probably smaller.

An obvious question is: With all these differences, what is the
difference in performance between IPv6 and IPv4? There is no simple
answer to this question. Since the IPv6 packet header is 20 bytes larger
than for IPv4, the raw payload throughput of a link carrying full sized
IPv6 packets is slightly less than for IPv4 (about 1.3% less for 1500
byte packets). However, many other factors come into play and
measurements often show better end-to-end performance for IPv6. For
example, in most countries
[Google statistics](https://www.google.com/intl/en/ipv6/statistics.html#tab=per-country-ipv6-adoption)
show lower latency (transit time) for IPv6. The safest summary is that
there is no significant performance difference.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Obsolete%20techniques.md) [<ins>Next</ins>](../04.%20Security/04.%20Security.md) [<ins>Top</ins>](03.%20Coexistence%20with%20Legacy%20IPv4.md)

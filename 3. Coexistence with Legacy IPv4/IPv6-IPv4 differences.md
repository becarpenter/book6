## IPv6 primary differences from IPv4

IPv6 is very similar for transit routers but has some considerable differences on the first hop for hosts as well as for routers.
The primary differences are:
- The first difference is very desirable and expected, IPv6 has a four times bigger address size (128bits against 32bits). SLAAC is more used on IPv6 than DHCP. SLAAC subnet is 64bits for historical reasons that are fixed in many standards. 2^64 hosts are not possible in one subnet but the address space is reserved even for a smartphone. Hence, it is disputable what is the effective IPv6 address space. It is bigger than 64bits but many IID bits are utilized for privacy and security, not for addressing per ser.
- NAT44 is a common solution in IPv4 networking.
NAT66 is discouraged by IETF and not specified as a standard. IPv6 end-to-end connectivity is considered a big value.
- IPv4 has only one address per interface (without special hacks).
Many IPv6 addresses on every interface are the norm. It is not just different address types (LLA, ULA, and GUA) but additionally many instances of GUA and ULA for security or virtualization reasons. The popular ChromOS has seven IPv6 addresses as the minimum. Additionally, the number of IPv6 addresses per interface could almost double in the case of link renumbering.
- IPv4 has only centralized DHCPv4 address acquisition.
IPv6 has additionally distributed address acquisition by SLAAC which is more adopted. SLAAC considerably changes the logic of the link operation.
- IPv4 has a complex (many fields) and theoretically variable header that is practically fixed because options are not widely used. 
IPv6 has a simple and fixed header. Additionally, IPv6 could have extension headers that permit unlimited protocol extensibility at the data plane. Many extension headers are already used in limited domains.
- IPv4 fragmentation is in the basic header and permitted in transit.
IPv6 fragmentation in the extension header and prohibited on the transit.
- IPv4 address resolution on the link by ARP protocol is at layer 2 (for the ethernet media it is ethernet frame). IPv6 address resolution on the link by ND protocol is at layer 3 (IPv6 packet over LLA or other IP addresses).
- Multicast is not needed for IPv4 itself.
Multicast is mandatory for the IPv6 link operation. Many ND functions are using multicast. That may create advantages (for Ethernet) and disadvantages (for many types of wireless).
The list above is not comprehensive, but the other differences are probably smaller.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Tunnels.md) [<ins>Previous</ins>](Obsolete%20techniques.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

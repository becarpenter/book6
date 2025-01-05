## Prefix per Host

IPv6 nodes very often have multiple valid addresses, for example by
configuring temporary addresses
\[[RFC8981](https://www.rfc-editor.org/info/rfc8981)\]. Since IPv6
address space is not a scarce resource, there are scenarios where
assigning a complete /64 prefix to an individual host may be
advantageous. Two mechanisms for this have been defined in
[RFC 8273](https://www.rfc-editor.org/info/rfc8273) and
[RFC 9663](https://www.rfc-editor.org/info/rfc9663).

One scenario where such a solution may be useful is a shared-access
network service where a Layer 2 access network (typically Wi-Fi) is
shared by multiple visiting subscriber devices. Service providers may
have a legal or operational requirement to provide isolation between
connected visitor devices, e.g. to control potential abuse of the shared
network. Separate prefixes make such isolation much simpler, since there
is no need to track multiple individual /128 addresses per host.

This approach has other benefits such as better scaling properties for
neighbor caches, etc., which are discussed in RFC 9663. The latter uses
standard DHCPv6 Prefix Delegation (DHCPv6-PD)
\[[RFC8415](https://www.rfc-editor.org/info/rfc8415)\], whereas RFC 8273
uses specially crafted Router Advertisement messages.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Address%20Planning.md) [<ins>Next</ins>](../06.%20Management%20and%20Operations/06.%20Management%20and%20Operations.md) [<ins>Top</ins>](05.%20Network%20Design.md)

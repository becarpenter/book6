## Packet size and Jumbo Frames

### Fragmentation

As already stated in
[3. IPv6 primary differences from IPv4](../3.%20Coexistence%20with%20Legacy%20IPv4/IPv6%20primary%20differences%20from%20IPv4.md),
IPv6 does not allow intermediate routers to fragment packets. Instead,
IPv6 pushes the responsibility of fragmentation to the source node. If a
packet exceeds the MTU, it is either fragmented by the sender or
dropped. This means the sender must use PMTUD
\[[RFC7690](https://www.rfc-editor.org/info/rfc7690)\] to ensure that
packets are sized appropriately for the smallest MTU along the path. The
sender fragments packets if necessary before sending them. This require
additional computation on the sender to fragment packets but there has
been no significant performance implication reported.

### MTU Size and Jumbo Frames

A jumbo frame is an Ethernet frame that is larger than the standard 1500
bytes, commonly configured to be around 9000 bytes. If a router along
the path has a smaller MTU when sending jumbo frames in an IPv4 network,
it will fragment the frame. This can lead to higher fragmentation
overhead because the larger the original frame, the more fragments it
must be split into. Additionally, fragmentation adds processing
complexity at both the router and the destination where reassembly
occurs.

IPv6 avoids this fragmentation overhead by relying on PMTUD
\[[RFC7690](https://www.rfc-editor.org/info/rfc7690)\]. If a jumbo frame
exceeds the MTU of any network hop, the sender is responsible for
fragmenting it before transmission. However, if properly configured, the
sender can send larger packets efficiently without fragmentation,
provided that the entire path supports jumbo frames. Ths allows IPv6 to
handle larger packets more effectively because the Path MTU Discovery
mechanism ensures that packets fit within the MTU of every hop along the
route. This mechanism is defined in
\[[RFC8201](https://www.rfc-editor.org/info/rfc8201)\].

The “Jumbo Payload Option” in IPv6
\[[RFC2675](https://www.rfc-editor.org/info/rfc2675)\] allows packets larger
than 65,535 bytes (the maximum payload size for standard IPv6 packets)
to be transmitted. This option is included in the Hop-by-Hop Options
header and enables IPv6 to support super jumbo frames efficiently, even
when dealing with extremely large packet sizes. This mechanism
simplifies the handling of large packets without requiring them to be
split into smaller fragments. If a network supports large enough MTUs,
IPv6 can use this option to transmit large frames without intermediate
fragmentation. However, it is very little used because it needs a layer
2 technology supporting very big packets. An interesting use case is for
_internal_ communication in support of segmentation offload, described in
[this blog entry](https://www.sipanda.io/post/segmentation-offload-and-protocols-let-s-be-friends).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Energy%20consumption.md) [<ins>Next</ins>](Basic%20Windows%20commands.md) [<ins>Top</ins>](6.%20Management%20and%20Operations.md)

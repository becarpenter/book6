## Packet Format

IPv6 packets are transmitted independently of each other even if they
belong to the same application session, so they are sometimes referred
to as *datagrams*. The basic datagram header is as follows. (The diagram
is 32 bits wide and big-endian.)

```
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version| Traffic Class |           Flow Label                  |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Payload Length        |  Next Header  |   Hop Limit   |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               |
   +                                                               +
   |                                                               |
   +                         Source Address                        +
   |                                                               |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               |
   +                                                               +
   |                                                               |
   +                      Destination Address                      +
   |                                                               |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

(Followed immediately by one or more "next headers" including the
upper layer payload.)
```

Some notes on these fixed fields:

- Version: is always 6

- Traffic class: six bits of
  [differentiated services](https://www.rfc-editor.org/info/rfc2474)
  code point followed by two
  [ECN](https://www.rfc-editor.org/info/rfc3168) bits. See
  [Traffic class and flow label](Traffic%20class%20and%20flow%20label.md).

- Flow label: 20 bits. Should be a pseudo-random value unique to a given
  traffic flow. See
  [Traffic class and flow label](Traffic%20class%20and%20flow%20label.md).

- Payload length: Length of the rest of the packet following this IPv6
  header, counted in bytes.

- Next header: an integer defining the type of the following header.

- Hop limit: counts down at each routing hop. Packet discarded when it
  hits zero.

- Addresses: 128 bits; see below.

The "next headers" are an important aspect of the design. After the
fixed header just defined, there are one or more additional headers
chained together. The best description is probably in
[the standard itself](https://www.rfc-editor.org/info/rfc8200), so we
only give a summary here. Every header format has a known length, and
includes a "next header" field identifying the next header (d'oh). The
last header in a packet is usually a TCP or UDP header containing the
actual payload. The last header naturally has a "next header" field, but
it contains the magic number 59, which means "no next header", and
terminates the chain.

(The standard seems to allow a packet which has 59 as the initial "Next
header" and therefore no extension headers and no payload. There is no
reason to lose sleep over this.)

The earlier headers have functions including:

- Hop-by-hop options, for packet-level options that should be examined
  by every node on the path.

- Fragment header, when a packet has been fragmented (which happens only
  at the source, if the raw packet exceeds the known MTU of the
  transmission path, which is at least the IPv6 minimum MTU of 1280
  bytes).

- Destination options, for packet-level options only useful at the
  destination node.

- Routing header, if non-standard routing is required.

- Encapsulating security payload, if
  [IPsec](https://www.rfc-editor.org/info/rfc4303) is in use.

An interesting feature of IPv6 is that extension header types are
numbered out of the same space as IP protocol numbers. It isn't a
coincidence that the next header type for UDP is 17, the same as
IPPROTO_UDP; it's by design. The latest set of valid extension header
types is always available from
[IANA](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml).

Extension headers and options are described in more detail in the
section
[Extension headers and options](Extension-headers-and-options.md). It's
also worth noting that Wireshark knows all about IPv6 header formats.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Addresses.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)

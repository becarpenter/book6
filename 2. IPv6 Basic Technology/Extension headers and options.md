## Extension headers and options

As explained in
[2. Packet Format](../2.%20IPv6%20Basic%20Technology/Packet%20Format.md),
every IPv6 packet may include one or more extension headers before the
transport layer payload (UDP, TCP, etc.). For the precise rules of how
extension headers and options are encoded, see
[STD 86](https://www.rfc-editor.org/info/std86). The current set of
standardized extension headers is listed at
[IANA](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml#extension-header).
Here are some notes on the most common ones:

- Hop-by-Hop (HBH) options, for packet-level options that should be
  examined by every node on the path. The defined options are listed,
  with references, at
  [IANA](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml#ipv6-parameters-2).
  Option 0x05 "Router Alert" is perhaps the most interesting; it is
  intended to warn every router on the path that the packet may need
  special handling. Unfortunately, experience shows that this extension
  header can be problematic, and that many routers do not in fact
  process it. Indeed,
  [RFC 8200](https://www.rfc-editor.org/info/rfc8200) states that "it is
  now expected that nodes along a packet's delivery path only examine
  and process the Hop-by-Hop Options header if explicitly configured to
  do so."

  Router Alert types have their own registry at
  [IANA](https://www.iana.org/assignments/ipv6-routeralert-values/ipv6-routeralert-values.xhtml).

- Fragment header, when a packet has been fragmented (which happens only
  at the source, if the raw packet exceeds the known MTU of the
  transmission path, which is at least the IPv6 minimum MTU of 1280
  bytes). IPv6 fragmentation is significantly different from IPv4
  fragmentation, which may occur anywhere along the path. The technical
  details are described in
  [STD 86](https://www.rfc-editor.org/info/std86). Of course,
  fragmentation interacts with PMTUD (Path Maximum Transmission Unit
  Determination) so the lazy solution is to never exceed the 1280 byte
  limit. For PMTUD, see [STD 87](https://www.rfc-editor.org/info/std87),
  [RFC 8899](https://www.rfc-editor.org/info/rfc8899), and (for horror
  stories) [RFC 7690](https://www.rfc-editor.org/info/rfc7690). Also see
  "IP Fragmentation Considered Fragile" for operational recommendations
  \[[BCP230](https://www.rfc-editor.org/info/bcp230)\].

- Destination options, for packet-level options only useful at the
  destination node. These are also listed at
  [IANA](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml#ipv6-parameters-2).

- Routing header, if non-standard routing is required. There are various
  [routing header types](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml#ipv6-parameters-2).
  An important current one is the Segment Routing Header (type 4,
  [RFC 8754](https://www.rfc-editor.org/info/rfc8754)). A router that
  acts as an intermediate destination and therefore processes routing
  headers is known as an 'intermediate node' in
  [STD 86](https://www.rfc-editor.org/info/std86).

- Encapsulating security payload, if
  [IPsec](https://www.rfc-editor.org/info/rfc4303) is in use. This is
  the defined mechanism for IPv6 security at layer 3. This is probably
  the most widely used IPv6 extension header.

Both hop-by-hop and destination options include flag bits in the option
type for nodes that may not understand the option, telling the node
whether to simply ignore the unknown option, or whether to drop the
whole packet and possibly send an ICMP response.

There is a recognized operational problem with IPv6 extension headers:
while they work well within a limited domain with consistent
administration and security rules, they are not reliably transmitted
across the open Internet, presumably due to firewall and router
filtering rules. [RFC 7872](https://www.rfc-editor.org/info/rfc7872)
reported on the situation in 2015, and there is ongoing work to update
similar measurements. The operational implications are described in
[RFC 9098](https://www.rfc-editor.org/info/rfc9098) and filtering
recommendations are in
[RFC 9288](https://www.rfc-editor.org/info/rfc9288).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Transport%20protocols.md) [<ins>Next</ins>](Traffic%20class%20and%20flow%20label.md) [<ins>Top</ins>](2.%20IPv6%20Basic%20Technology.md)

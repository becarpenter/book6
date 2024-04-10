## Traffic class and flow label

The Traffic Class in every IPv6 packet is a byte also known as the
Differentiated Services field. It is treated in every respect exactly
like the same field in every IPv4 packet (originally named the TOS octet
in [RFC791](https://www.rfc-editor.org/info/rfc791)). It contains six
bits of
[differentiated services](https://www.rfc-editor.org/info/rfc2474) code
point followed by two
[ECN (Explicit Congestion Notification)](https://www.rfc-editor.org/info/rfc3168)
bits. [RFC8100](https://www.rfc-editor.org/info/rfc8100) gives a good
overview of current differentiated service interconnection practices for
ISPs. [RFC5127](https://www.rfc-editor.org/info/rfc5127),
[RFC4594](https://www.rfc-editor.org/info/rfc4594),
[RFC5865](https://www.rfc-editor.org/info/rfc5865),
[RFC8622](https://www.rfc-editor.org/info/rfc8622) and
[RFC8837](https://www.rfc-editor.org/info/rfc8837) also describe current
practice.

ECN is intended for use by transport protocols to support congestion
control.

The Flow Label is a 20 bit field in every IPv6 packet, although as its
name indicates, it is only relevant to sustained traffic flows. The
sender of a packet should fill it with a pseudo-random non-zero value
unique to a given traffic flow, such as a given TCP connection. It can
then be used downstream in support of load balancing. By definition, the
20 bits have no semantics, although some deployments are known to have
broken this guideline, which would interfere with load balancing. See
[IPv6 Flow Label Specification](https://www.rfc-editor.org/info/rfc6437),
[Using the IPv6 Flow Label for Equal Cost Multipath Routing and Link Aggregation in Tunnels](https://www.rfc-editor.org/info/rfc6438)
and
[Using the IPv6 Flow Label for Load Balancing in Server Farms](https://www.rfc-editor.org/info/rfc7098).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Extension%20headers%20and%20options.md) [<ins>Next</ins>](Source%20and%20Destination%20Address%20Selection.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)

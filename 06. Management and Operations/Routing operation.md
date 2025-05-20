## Routing operation

### Global Routing

Global routing between service providers using multiprotocol BGP-4
\[[RFC2545](https://www.rfc-editor.org/info/rfc2545),
[RFC 4271](https://www.rfc-editor.org/info/rfc4271),
[RFC 4760](https://www.rfc-editor.org/info/rfc4760)\]
is a highly specialized topic,
not for amateurs, that will not be summarized here.
An excellent source is Iljitsch van Beijnum's book
[Internet Routing with BGP](https://www.iljitsch.com/2022/11-18-new-e-book-internet-routing-with-bgp.html)
(2022). For relevant RFCs and upcoming drafts, see 
[the IETF GROW working group](https://datatracker.ietf.org/wg/grow/documents/),
which covers both IPv6 and IPv4 BGP operations.

### Carrier, Enterprise and Campus Networks

Carriers (Internet service providers) and very large enterprises
typically operate iBGP
\[[RFC4456](https://www.rfc-editor.org/info/rfc4456)\],
IS-IS \[[RFC5308](https://www.rfc-editor.org/info/rfc5308),
[RFC 7775](https://www.rfc-editor.org/info/rfc7775)\],
or OSPFv3 \[[RFC5340](https://www.rfc-editor.org/info/rfc5340)\]
for IPv6. 

Most enterprise networks or campus networks typically operate
OSPFv3 \[[RFC5340](https://www.rfc-editor.org/info/rfc5340)\]
or IS-IS \[[RFC5308](https://www.rfc-editor.org/info/rfc5308),
[RFC 7775](https://www.rfc-editor.org/info/rfc7775)\] for IPv6.

A brief introduction to OSPFv3 usage is at the
[Blueally blog](https://www.blueally.com/ipv6-deployment-series-part-3-ospfv3/).

Not everyone can attend the RIPE NCC _Advanced IPv6_ training course,
but everyone can download their excellent 264 slides, which cover
OSPF and BGP configuration and many other things:
[download 37MB](https://www.ripe.net/documents/3822/AdvancedIPv6-Slides_xDUF4U9.pdf).

A video introduction to IS-IS (for all address families) from Cisco is
[on Youtube](https://youtu.be/jWdD8SCwzHk).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Benchmarking%20and%20monitoring.md) [<ins>Next</ins>](Security%20operation.md) [<ins>Top</ins>](06.%20Management%20and%20Operations.md)

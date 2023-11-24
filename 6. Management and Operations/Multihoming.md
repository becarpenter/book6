## Multihoming

Multihoming means configuring a site in such a way that it is connected
via more than one link to the Internet, preferably via different ISPs,
usually to provide redundancy in case of failures. The phrase
"multihoming with multiple providers" (MHMP) is sometimes used. The
previous section describes the problems with achieving MHMP using
multiple address prefixes. This section describes practical techniques
for site multihoming.

Note that the term "multihoming" is sometimes used to describe a
configuration _inside_ a site network where a node is connected to more
than one internal router to provide redundancy. That complicates site
routing, and is not the topic here.

In 2003, the IETF established goals for site multihoming
\[[RFC3582](https://www.rfc-editor.org/info/rfc3582)\]. In summary, the
main goals were: redundancy, load sharing, performance, policy control,
simplicity, and transport session survivability. Without describing all
the efforts made since then, it is clear that a solution that satisfies
all these goals simultaneously has been difficult to find.

Today, the most practical approach for a large site, or for a large
enterprise network distributed over multiple physical sites, is to
obtain a provider-independent (PI) prefix from the appropriate Internet
address registry, which will typically be a /48 prefix such as
`2001:db8:face::/48`. Then all hosts in the enterprise network that
require Internet access will be assigned IPv6 addresses within that
prefix. They might also be assigned Unique Local Addresses (ULAs) for
internal use, or IPv4 addresses, or both. The enterprise will then
select at least two ISPs to provide redundant connectivity to the
Internet, and arrange for both of them to advertise a BGP-4 route to
that prefix.

Internal routing must be arranged to direct traffic as required, using
routing metrics that favor one ISP or another, or spread the load, as
desired. When the egress to a particular ISP fails, backup routes to an
alternative egress router will take over. An additional advantage to the
enterprise is that address renumbering will never be required, since the
/48 prefix is tied to the enterprise, not to one of their ISPs.

This method is tried and tested. However, there are two reasons why it
cannot be extended indefinitely to cover smaller enterprises or even
domestic users. Firstly, it is significantly more costly than a single
provider-assigned (PA) prefix, and requires some level of operational
management by skilled technicians. Secondly, the wide area BGP-4 routing
system is widely considered unable to cope with the millions of PI
prefixes that would ensue if a majority of small and medium enterprises
adopted this solution. In November 2023, the global BGP-4 system carries
about 200,000 routes. There are estimated to be 32 million small
businesses in the USA alone, and 200 million in the world. If every
small business had its own PI prefix, the Internet would stop working.

Therefore, except for some thousands of large enterprises, any viable
solution for multihoming must be based on PA addresses.

_Work in progress, to be continued..._

RFC 7157

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Multi-prefix%20operation.md) [<ins>Next</ins>](Energy%20consumption.md) [<ins>Chapter Contents</ins>](6.%20Management%20and%20Operations.md)

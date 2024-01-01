## Multihoming

Multihoming means configuring a site in such a way that it is connected
via more than one link to the Internet, preferably via different ISPs,
usually to provide redundancy in case of failures. The phrase
"multihoming with multiple providers" (MHMP) is sometimes used.
[<ins>The previous section</ins>](Multi-prefix%20operation.md) describes
the problems in achieving MHMP using multiple address prefixes. This
section discusses practical techniques for site multihoming.

Domestic or very small office installations are out of scope for this topic. They
are rarely connected permanently to more than one ISP, and therefore cannot
expect smooth failover. They might have an alternative connection
(e.g., a wireless hot spot instead of a terrestrial connection) but the
changeover would amount to a network restart and would likely be manual.

Note that the term "multihoming" is sometimes used to describe a
configuration _inside_ a site network where a node is connected to more
than one internal router to provide redundancy. That complicates site
routing, and is not the topic here.

In 2003, the IETF established goals for site multihoming
\[[RFC3582](https://www.rfc-editor.org/info/rfc3582)\]. In summary, the
main goals were: redundancy, load sharing, performance, policy control,
simplicity, and transport session survivability. Without describing all
the efforts made since then, it is clear that a solution that satisfies
all these goals simultaneously has been difficult to find. A more recent
overview can be found in
[RFC7157](https://www.rfc-editor.org/info/rfc7157).

### Large sites

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
adopted this solution. In November 2023, the global BGP-4 system carried
about 200,000 IPv6 routes. There are estimated to be 32 million small
businesses in the USA alone, and 200 million in the world. If every
small business suddenly had its own PI prefix, the Internet would stop
working.

### Small or medium sites

Except for some thousands of large enterprises, a viable solution for
multihoming of small or medium enterprises must be based on PA
addresses, if it is to be used by millions of sites. However, as shown
in [<ins>the previous section</ins>](Multi-prefix%20operation.md),
operating with more than one PA prefix at the same time is currently
impractical, especially if transport session survivability is required.

The IETF has made various attempts to solve this problem, including the
SHIM6 protocol \[[RFC5533](https://www.rfc-editor.org/info/rfc5533)\]
and the Multiple Provisioning Domain Architecture
\[[RFC7556](https://www.rfc-editor.org/info/rfc7556)\]. Such methods
have not been successfully deployed. Other options, such as centralizing
redundant connections for a large corporate network at a single site, or
deploying application layer proxies to decouple internal and external
addressing, remain out of reach for small or medium enterprises.

If we abandon the goal of transport session survivability, so that
applications will have to recover from broken transport connections
after a multihoming failover, the problem is simplified. It should be
noted that essentially all mass market client applications already
handle such disconnects, which are commonplace when mobile or portable
devices move from place to place. This leads to one possible approach to
multihoming for small sites, which is essentially to do nothing except
connect the site to two (or more) ISPs and assign two (or more) PA
prefixes, and leave client applications to find a working path by trial
and error. This is essentially a generalization of the Happy Eyeballs
approach \[[RFC8305](https://www.rfc-editor.org/info/rfc8305)\], but it
will lead to help desk calls in the case of applications that are not
sufficiently resilient. It is clearly not sufficient for a large site,
especially if it operates servers as well as client hosts.

An approach that should avoid some of these help desk calls, but is not
currently favored by the IETF, is to used dynamic network prefix
translation, known as NPTv6
\[[RFC6296](https://www.rfc-editor.org/info/rfc6296)\],
\[[3. Translation and IPv4 as a service](../3.%20Coexistence%20with%20Legacy%20IPv4/Translation%20and%20IPv4%20as%20a%20service.md)\].
In this model, a translator is placed at the site exit router towards
each ISP. Outgoing and incoming packets are translated to and from
appropriate PA addresses. The routeable prefix part of each address is
changed, and possibly some bits in the IID, in a way that avoids transport
checksum errors. This translation is stateless and reversible, so causes
much less difficulty than traditional NAT; no port translation is
needed.

To simplify the translation processs, internal hosts (both clients and
servers) would be assigned Unique Local Addresses (ULAs)
\[[RFC4193](https://www.rfc-editor.org/info/rfc4193)\] that would rarely
change. However, servers will be announced to the outside world via DNS
using their translated PA addresses.

This method is known to have been successfully tested, although not
recommended by the IETF. It should be noted, however, that NPTv6 does
not share all the disadvantages of IPv4 NAT. As discussed in RFC 6296,

- NPTv6 does not need to translate port numbers, and it is
  checksum-neutral, so the transport layer is effectively unaffected.

- Translation is stateless, so matters such as asymmetric routing, load
  sharing, and router fail-over are not affected.

- Filtering of unwanted traffic requires an adequate firewall, but this
  is true for any serious IPv6 (or IPv4) deployment.

- Topology hiding, which is sometimes cited as an argument for NAT, is
  discussed in
  \[[4. Topology obfuscation](../4.%20Security/Topology%20obfuscation.md)\].
  NPTv6 does indeed largely obfuscate local topology. For example (again
  following RFC 6296), a host whose actual address is
  `fd01:0203:0405:0001::1234` might appear on the Internet as
  `2001:db8:0001:d550::1234`. An attacker that does not know the site's
  ULA prefix (`fd01:0203:0405::/48`) cannot reverse the translation and
  deduce the actual subnet prefix.

Of course, NPTv6 retains some of the disadvantages of NAT: all of the
problems that directly follow from having different IP addresses at the
two ends of a connection. Section 5 of
[RFC6296](https://www.rfc-editor.org/info/rfc6296) discusses this.
Any site running NPTv6 must either deal with
these problems, or avoid any affected applications. In particular,
SIP (Session Initiation Protocol for IP telephony) will not work without
the support of a proxy mechanism 
\[[RFC6314](https://www.rfc-editor.org/info/rfc6314)]
as well as provision for IPv6/IPv4 coexistence
\[[RFC6157](https://www.rfc-editor.org/info/rfc6157)].
This limits the applicability of NPTv6.

### Transport layer solutions

Another possible approach to site multihoming is to treat it as a
transport layer problem. If a transport protocol is agile enough to use
multiple paths (i.e., multiple source/destination address pairs),
failures at the network layer can be hidden. Multipath TCP (MPTCP,
\[[RFC8684](https://www.rfc-editor.org/info/rfc8684)\]) is defined but
not widely available. A multipath version of QUIC is under discussion,
as is a versatile API for the transport layer that would support
multipath solutions. Discussion continues in the IETF.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Multi-prefix%20operation.md) [<ins>Next</ins>](Energy%20consumption.md) [<ins>Chapter Contents</ins>](6.%20Management%20and%20Operations.md)

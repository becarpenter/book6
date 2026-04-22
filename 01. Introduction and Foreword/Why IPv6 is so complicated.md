## Why IPv6 is so complicated

There's no question that IPv6 is more complicated than IPv4, and people
sometimes ask why that is. Surely it would have been much simpler to
just add an extra 32 bits to the IPv4 address, and change nothing else?
In fact, every year or two people propose alternatives to IPv6 ("IPv8"
is a generic name for such proposals, which mainly involve 8-byte
addresses) because they have asked themselves that question. This note
attempts to answer the question, and to show why such proposals are a
waste of everybody's time, especially for the people who propose them.

There are at least three possible answers:

1. Just adding bits to the address isn't as simple as it seems.

1. IPv4 was not the only network layer protocol in the world in 1994,
   and the others had good features that IPv4 lacked.

1. The IPv6 designers went mad.

We will discuss each of these points in turn. To set the context, note
that the decision to develop IPv6 rather than one of the other possible
options was announced at the July 1994 IETF meeting in Toronto, Canada.
This followed a long process that formally started at an IAB workshop in
1991 \[[RFC1287](https://www.rfc-editor.org/info/rfc1287)\] and led to
an IESG report on future routing and addressing in late 1992
\[[RFC1380](https://www.rfc-editor.org/info/rfc1380)\]. Concerns about
routing led to classless addressing and BGP4 routing; concerns about
address exhaustion led to agreement that a new version of IP was needed.
But scaling up the routing and addressing systems were not the only
concerns in RFC 1380 (see point 2 above):

```
   Although the catalog of problems above is pretty complete as far as
   the scaling problems of the Internet are concerned, there are other
   Internet layer issues that will need to be addressed over the coming
   years.  These are issues regarding advanced functionality and service
   guarantees in the Internet layer.
 
   In any attempt to resolve the Internet scaling problems, it is
   important to consider how these other issues might affect the future
   evolution of Internet layer protocols.
```

In any case, various proposals for the new version were drafted in
1991/93 and the IETF had no clear direction. A BOF named "IPDECIDE" was
held at the July 1993 IETF meeting in Amsterdam, The Netherlands. Its
goal was to pick a direction, but the result was, um, indecisive. Next,
the IESG decided to set up an IP Next Generation (IPng) Directorate
under two Area Directors (Scott Bradner and Allison Mankin) to support
the decision process. This led to the July 1994 choice, guided by
\[[RFC1726](https://www.rfc-editor.org/info/rfc1726)\], and explained in
detail by \[[RFC1752](https://www.rfc-editor.org/info/rfc1752)\] and by
the book _IPng: Internet Protocol Next Generation_, S. Bradner and A.
Mankin (editors), Addison-Wesley, 1995.

### Why adding bits isn't simple

IPv4 implementations, in 1994 and still today, have the 32-bit address
format built into their code. Whether you expand the address size to 33,
64 or 128 bits, all IPv4 implementations will discard the packets. So
it's a matter of mathematical and physical fact that to expand the
address size, you must change the protocol, and that means two things
immediately:

1. You have to change the version number.

1. You have to add new code to handle the new version.

Furthermore, you don't want to split the Internet in two, so you must
design a method of interworking between the old version and the new
version. Annoyingly, you need to do that in a way that can be done
completely in machines that know about the new version, because other
machines don't know anything at all about the new version, by
definition. So,

3. You need a coexistence technique so that updated systems, with the
   new protocol, can connect to old systems that know nothing of the new
   protocol.

Two minutes of thought show that this third requirement has only two
solutions:

&#8195;3A. Dual stack, in which the new machines speak both the old (IPv4) and
new (IPng) protocol.

&#8195;3B. Translation, in which something translates addresses between the
old and new protocols.

This has been known for more than 30 years
\[[RFC1671](https://www.rfc-editor.org/info/rfc1671)\], although people
still sometimes try to deny it.

To state this in graphical form, here's a diagram, showing who can talk
to who, assuming the simplistic model of IPng with 64 bit addresses:

```
              OLD    DUAL   NEW     
            ----------------------
        OLD |  32  |  32  |  XX  |      
            |------|------|------|
       DUAL |  32  |  64  |  64  |
            |------|------|------|
        NEW |  XX  |  64  |  64  |
            ----------------------
```

Protocol details, and the exact address length, don't matter. The XX
cases can only work with protocol and address translation. All the
complexities (and that really means all) of IPv4-IPng coexistence and
transition are a result of this diagram, and the details of IPng design
do not change this fact of nature.

Any purported design of a "better" or "simpler" IPng than IPv6 does not
change this, however hard its authors try. In other words, the basic
difficulties of IPv6 transition and coexistence have nothing to do with
the design of IPv6.

Incidentally, "IPv8" proponents often ask why IPv6 didn't simply stick
some extra bits on the front of IPv4 addresses, instead of inventing a
whole new format. Actually, we tried that: the "IPv4-Compatible IPv6
address" format was defined in
\[[RFC3513](https://www.rfc-editor.org/info/rfc3513)\] but deprecated by
\[[RFC4291](https://www.rfc-editor.org/info/rfc4291)\] because it turned
out to be of no practical use for coexistence or transition. The related
"IPv4-Mapped IPv6 address" format is still valid and has a role in the
POSIX socket API. Mappings of this kind also figured in the moderately
successful coexistence technologies known as 6to4
\[[RFC3056](https://www.rfc-editor.org/info/rfc3056),
[RFC3068](https://www.rfc-editor.org/info/rfc3068)\] and Teredo
\[[RFC4380](https://www.rfc-editor.org/info/rfc4380)\], which have now
been overtaken by events.

Finally, it's worth remembering that IPv4 is itself no longer simple.
Compared with 1994, we now have a whole lot of complications:
subscriber-side NAT, carrier-grade NAT, firewalls, IPsec, VPNs,
Differentiated Services, link-local addresses, content distribution
networks, etc.

### The protocol zoo

In the early 1990s, the Internet had not yet conquered the world (after
all, the World Wide Web hardly existed before 1993) and there were many
alternatives to IPv4 in use. Also, one of the most growly protocols in
the zoo was wearing a smart business suit and lived in Switzerland with
its rich friends - most governments and big businesses believed that the
future network was certain to use the official international standard
Open Systems Interconnection protocol suite. To many people it seemed
inevitable that an OSI network layer would replace IPv4. At the same
time, there were numerous proprietary network layer protocols in use.
All the IETF had to offer were various competing IPng proposals, not
even running code! All these other existing protocols had juicy features
that IPv4 did not provide. Whatever IPng would be, it was expected to
have at least some new features; plain IPv4 with bigger addresses was
not what people expected or wanted.

Looking back, this was probably unfortunate, but it was a fact. IPng had
to be better than IPv4, DECNET, Novell Netware, etc., and above all
_better than OSI_.

### Did the IPv6 designers go mad?

That might be going a bit far, so the question should probably be: Did
the IPv6 design suffer from Second System Syndrome,
["the tendency for a successful first system (often small and relatively elegant) to be followed by a second system that becomes over-engineered or bloated"](https://en.wikipedia.org/wiki/Second-system_effect)?
Did we add stuff for its own sake?

The objective answer is "not much." First of all, IPv6 really is a
conservative design - it doesn't change the basic IP model of
connectionless packet switching with topological addresses. We added the
flow label (harmless if unused, as it was for many years). We tweaked
the fragmentation mechanism. We replaced IPv4 "options" with IPv6
"extension headers". (Just as IPv4 options are largely unused, so are
IPv6 extension headers, except within limited domains.) Most important,
we _added_ Stateless Address Autoconfiguration (SLAAC) and the closely
linked router advertisement (RA) mechanism, and the linked idea of an
interface identifier (IID) as part of the address. SLAAC was inspired by
DECNET, Netware and Appletalk, none of which required manual address
configuration. SLAAC is partly redundant with DHCPv6, and the reason for
that is that DHCP was new and unproven when SLAAC and RA were designed;
DHCPv6 was actually a retrofit.

The author was too closely involved to say whether these changes and
additions amounted to Second System Syndrome, but they were certainly
not gratuitous changes. They have not caused most of the problems during
IPv6 deployment; those almost all come from the area of IPv4/IPv6
coexistence.

There was also unnecessary confusion caused by a rather political
decision to make IPv6 _require_ support for IP Security (IPsec), which
was an immature technology at the time. This was a definite brake on
IPv6 deployment until it was dropped after some years.

### Do not make things worse

It's worth adding that some of the "IPv8" proposals over the years have
included ideas that would make things worse rather than better - things
like geographic addressing, address prefixes based on Autonomous System
numbers, addresses with semantics encoded in their bits, and the list
goes on. All these things would break Internet routing, make site
renumbering even harder, risk running out of addresses yet again,
simplify pervasive surveillance, or cause other forms of operational
harm. (To take one example, although geographic addressing has some
obvious advantages when geolocation is wanted, it is incompatible with
the way Internet interdomain routing works.)

### It would take 25 years anyway

Getting IPv6 to about 50% deployment has taken more than 25 years. Any
alternative or new proposal would be the same. Setting aside IPv6,
consider that all of the following examples have taken decades, not
years, to deploy Internet-wide:

1. Retiring frame relay
1. Replacing ATM
1. Deploying DNSSEC
1. Deploying RPKI

### Conclusion

The main reason for IPv6, and its only real reason for existence, was
bigger addresses. The problems of coexistence were inevitable, and it
was hard to find the best (or rather, least bad) solutions. Most of the
difficulties of IPv6 implementation and deployment are not the result of
the details of IPv6 design. Any address length greater than 32 would
create all the coexistence and transition problems we have experienced
since 1994. Both dual stack deployment and translation (of protocol plus
addresses) were mathematically inevitable. No alternative choice can
possibly avoid these issues.

The community should think carefully before investing time and resources
in such proposals.

### Postscriptum

For the record, here are some of the proposals made over the years.

Steve Deering, 1992, "The Simple Internet Protocol" (SIP), an early IPng
candidate, had 8-byte addresses. SIP was assigned version number 6. It
was only fully documented in 2018
\[[RFC8507](https://www.rfc-editor.org/info/rfc8507)\].

Paul Francis, 1992, "The 'P' Internet Protocol" (PIP), an IPng candidate
\[[RFC1621](https://www.rfc-editor.org/info/rfc1621),
[RFC1622](https://www.rfc-editor.org/info/rfc1622)\] was _officially_
IPv8 for a while. It had variable length addresses.

Bob Hinden and Steve Deering 1993/4, "Simple Internet Protocol Plus"
(SIPP), an IPng candidate
\[[RFC1710](https://www.rfc-editor.org/info/rfc1710)\], had 8-byte
addresses. It inherited SIP's use of version number 6. At the end of the
IPng decision process, it mutated to 16-byte addresses and was the
immediate precursor of IPv6.

\[[draft-carpenter-aeiou](https://datatracker.ietf.org/doc/draft-carpenter-aeiou/)\]
(1994)

Jim Fleming touted "IPv8" and "IPv16" starting in 1996, but we have not
found a coherent technical description of them. The best we have found
is a cryptic statement at
[AFNOG](https://afnog.org/archives/archives/msg01304.html):

```
IPv8 and IPv16 addresses are encoded in the **right-most 64-bits** of the 128-bit DNS.  The left-most 64-bits
are used for transition mechanisms.
```

\[[draft-terrell-ip-spec-ipv7-ipv8-addr-cls](https://datatracker.ietf.org/doc/draft-terrell-ip-spec-ipv7-ipv8-addr-cls/)\],
\[[draft-terrell-logic-analy-bin-ip-spec-ipv7-ipv8](https://datatracker.ietf.org/doc/draft-terrell-logic-analy-bin-ip-spec-ipv7-ipv8/)\]
(1999)

\[[draft-shyam-real-ip-framework](https://datatracker.ietf.org/doc/draft-shyam-real-ip-framework/)\]
(2014)

\[[draft-omar-ipv10](https://datatracker.ietf.org/doc/draft-omar-ipv10/)\]
(2016)

\[[draft-sambana-irtf-internet-protocol-sixteen](https://datatracker.ietf.org/doc/draft-sambana-irtf-internet-protocol-sixteen/)\]
(2022)

\[[draft-thain-ipv8](https://datatracker.ietf.org/doc/draft-thain-ipv8/)\]
(2026)

\[[draft-hause-asip](https://datatracker.ietf.org/doc/draft-hause-asip/)\]
(2026)

Here's an
[interesting blog](https://www.ip.network/blog/what-is-ipv8-protocol).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Why%20version%206.md) [<ins>Next</ins>](../02.%20IPv6%20Basic%20Technology/02.%20IPv6%20Basic%20Technology.md) [<ins>Top</ins>](01.%20Introduction%20and%20Foreword.md)

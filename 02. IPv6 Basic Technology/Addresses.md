## Addresses

A 128 bit address is big enough that, assuming the adoption of wise
allocation policies, IPv6 will [never](https://m.xkcd.com/865/) run out
of addresses. However, the reason for choosing 128 rather than 64 was
not just that: it was also to allow for some intrinsic structure to
addresses, as described below. On the other hand, a *fundamental*
property of IPv6 unicast routing is that it is
[based on all 128 bits](http://www.rfc-editor.org/info/bcp198),
regardless of any internal structure. In other words, a unicast routing
prefix is anywhere between 1 and 128 bits long. There is more about
[routing](Routing.md) below.

_Terminology note_: When comparing two address prefixes, a _longer_
prefix covers a smaller amount of address space (e.g., a 52-bit prefix
covers a 76-bit address space) and a _shorter_ prefix covers a larger
amount (e.g., a 48-bit prefix covers an 80-bit address space).
Unfortunately, some documents use the term "larger prefix", which is
ambiguous.

The enormous amount of IPv6 address space allows a good deal of freedom
in network design that never existed for IPv4. This is discussed in
\[[5. Network Design](../05.%20Network%20Design/05.%20Network%20Design.md)\].

The IPv6 addressing architecture is defined by
[RFC 4291](http://www.rfc-editor.org/info/rfc4291), which has not been
fundamentally revised since 2006, although there are a number of RFCs
that partially update it.

### Notation

We'll first introduce the notation for writing down IPv6 addresses, and
then use that notation to explain the main features.

The only feasible way to write down 128 bit addresses is in hexadecimal.
There's no doubt this is less convenient than the decimal notation used
for IPv4, but that's unavoidable. Despite what you may see in older
RFCs,
[the recommendation by RFC5952 today](https://www.rfc-editor.org/info/rfc5952)
is to use lower-case letters for hexadecimal. Thus a basic example of
the notation is:

```
2001:0db8:ef01:2345:6789:abcd:ef01:2345
```

In that example, there are 8 groups of 4 hexadecimal digits, to specify
all 128 bits in 16 bit chunks. In conventional hexadecimal notation,
that would be `0x20010db8ef0123456789abcdef012345`. The colons (':') are
there to help the reader.

In each chunk of 16 bits, leading zeros are dropped, so we write:

```
2001:db8:ef01:45:6789:abcd:ef01:2345
```

**not**:

```
2001:0db8:ef01:0045:6789:abcd:ef01:2345
```

There is often a run of zero bytes in an IPv6 address. One such run can
be replaced by a double colon ('::') so that we write:

```
2001:db8::6789:abcd:ef01:2345
```

**not**:

```
2001:db8:0:0:6789:abcd:ef01:2345
```

The idea is that IPv6 addresses should be cut-and-pasted in almost all
cases. If you ever do have to enter one manually, a great deal of care
is needed. Note that not all implementations will strictly follow
RFC9592, and older documentation often uses uppercase hexadecimal.

The choice of ':' as the separator is annoying in one particular aspect
\- where a colon has another meaning and works as a separator between
address and port. This is quite common in (Web) URLs, that's why IPv6
addresses in URLs are in square brackets like this:

```
https://[2001:db8:4006:80b::200e]:443
```

### Address registries

The top-level address registries are maintained by IANA
(the Internet Assigned Numbers Authority) in the
[IPv6 Address Space registry](https://www.iana.org/assignments/ipv6-address-space/ipv6-address-space.xhtml)
and several subsdidiary registries linked from that page.

Regional address assignments are maintained by the RIRs (Regional Internet Registries) as described on the [IANA web site](https://www.iana.org/numbers). RIRs in turn assign address space to Internet service providers, national registries, or local registries.

### Easy addresses

The unspecified IPv6 address is simply zero, represented as `::`.

The loopback IPv6 address is 1, represented as `::1`. Note that IPv6
only has one loopback address whereas IPv4 has `127.0.0.0/8` reserved
for loopback addressing. It seems that some operators have misused
address such as `::2` or `::3` as if they were loopback addresses; this
is a misconfiguration.

### Routeable unicast addresses

This is the most familiar case. A unicast address is split into a
routing prefix followed by an interface identifier (IID). The normal
case is a 64 bit prefix that identifies a subnet, followed by a 64 bit
IID. Thus:

```
 ----- prefix ----  IID
 |               |  |  |
 2001:db8:4006:80b::cafe
```

However, that's a bad example because 'cafe' might be guessable. For
privacy reasons, a pseudo-random IID is
[strongly recommended](https://www.rfc-editor.org/info/rfc8064):

```
 ----- prefix ---- ------- IID -------
 |               | |                 |
 2001:db8:4006:80b:a1b3:6d7a:3f65:dd13
```

This replaces a deprecated mechanism of forming the IID based on IEEE
MAC addresses. Many legacy products still use that mechanism.

In this example, we used a 64 bit prefix based on the `2001:db8::/32`
prefix, which is reserved for documentation use, but at present all
prefixes
[allocated to the Regional Internet Registries](https://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xhtml)
start with a 2. Often such addresses are referred to as GUAs (globally
reachable unique addresses). The background to prefix assignment
policies by the registries is covered by
[BCP 157](https://www.rfc-editor.org/info/bcp157).

(Incidentally, `2001:db8::/32` is the full notation for a 32-bit prefix,
but sometimes it is written informally as `2001:db8/32`, leaving the
reader to insert the missing '::'.)

GUAs are often described as belonging administratively to one of two
classes, PI or PA. Provider Independent (PI) address prefixes are those
that have been assigned directly to an end-user site by one of the
address registries. Provider Assigned (PA) address prefixes are those
that have been assigned to an end-user site by one of its Internet
Service Providers. PI prefixes are valid even if the site changes to a
different service provider; PA prefixes vanish if the site drops the ISP
concerned, and some ISPs change a site's PA prefix from time to time
without warning. The benefit of PA addresses is that all of a given
ISP's customer prefixes can be aggregated into a single BGP-4
announcement, thus greatly reducing growth in the Internet's global
routing tables. By contrast, each new PI prefix adds to the global
routing tables. For this reason, it is unacceptable for millions of
sites to use PI prefixes.

Another type of routeable unicast address exists, known as Unique Local
Addresses (ULA). The benefits of these are:

1. They are self-allocated by a particular network for its own internal
   use.
1. They are all under a /48 prefix that includes a locally assigned
   *pseudo-random* 40 bit part.
1. They **MUST NOT** be routed over the open Internet, so remain
   private.

An example:

```
 ----- prefix --- ------- IID -------
 |              | |                 |
 fd63:45eb:dc14:1:a1b3:6d7a:3f65:dd13
```

The 'fd' prefix is enough to identify a ULA. In this example,

- `fd63:45eb:dc14::/48` is the so-called ULA prefix.
- The locally generated pseudo-random part is `0x6345ebdc14`.
- `fd63:45eb:dc14:1::/64` is the subnet prefix.

Occasionally people use the prefix `fd00::/48` (zero instead of the
pseudo-random bits) but this is not recommended. If two such networks
are merged, things will break.

It is slightly confusing that both GUAs and ULAs are architecturally
defined as having 'global scope', but ULAs are forbidden *by rule* to be
routed globally.

In the preceding examples, the prefix boundary is shown after bit 63
(counting from zero), so the subnet prefix is `2001:db8:4006:80b/64` or
`fd63:45eb:dc14:1/64`. This is the normal setting in IPv6: subnets have
64 bit prefixes and 64 bit IIDs.
[Automatic address configuration](Auto-configuration.md) depends on this
fixed boundary. Links that don't use automatic address configuration are
not bound by the /64 rule, but a lot of software and configurations rely
on it.

An important characteristic of routeable IPv6 unicast addresses is that
they are assigned to interfaces (not whole nodes) and each interface may
have several addresses at the same time. For example, a host in an
enterprise network could in theory have all of the following
simultaneously:

- A fixed GUA with a DNS entry for it to act as a web server
- A temporary GUA with a random IID for it to act as a client for remote
  web access \[[RFC8981](https://www.rfc-editor.org/info/rfc8981)\]
- A fixed ULA used for transactions within the enterprise
- A second fixed GUA under a different prefix, with a DNS entry, for
  backup

You may see multiple temporary GUA addresses with random IID when you
have some long-running TCP sessions, e.g. ssh, and your system created
new addresses while the session(s) were up and running.

However, making the last two settings (GUA plus ULA, or two GUA
prefixes) work smoothly can be challenging and is discussed in
[6. Multi-prefix operation](../06.%20Management%20and%20Operations/Multi-prefix%20operation.md).

### Anycast addresses

Syntactically, anycast addresses are identical to unicast addresses, so
any GUA or ULA may be treated as anycast. A special case is that on a
link with prefix P, the address P::/128 (i.e. with the IID set to zero)
is the subnet-router anycast address. Here is an example:

```
 ----- prefix ----
 |                |
 2001:db8:4006:80b::
```

### Link local addresses

These look like:

```
prefix ------- IID -------
 |    ||                 |
 fe80::a1b3:6d7a:3f65:dd13
```

The `fe80::/64` prefix is enough to identify a link local address.

Link local addresses (LLAs) do what it says on the can: they are *never*
forwarded by a router (but they will be forwarded by a Layer 2 switch).
They are essential during the startup phase for address allocation and
they are essential for reaching a first-hop router.

LLAs are specific to a given interface, and a host with multiple Layer 2
interfaces will have a different address on each one. There's a special
notation for this, e.g.:

```
prefix ------- IID ------- zone
 |    ||                 | |  |
 fe80::a1b3:6d7a:3f65:dd13%eth0

or

 fe80::a1b3:6d7a:3f65:dd13%7
```

The first of these would be seen on, say, a Linux host and the second on
a Windows host; the character(s) after the '%' sign are the Layer 2
interface's locally defined identifier. Unfortunately, that makes two
'identifiers' in one address. Technically, the second one can be
referred to as the 'Zone ID' according to
[RFC 4007](https://www.rfc-editor.org/info/rfc4007). User interfaces
need to accept the Zone ID in some use cases
\[[RFC9844](https://www.rfc-editor.org/info/rfc9844)\]. Unfortunately,
current web browsers do not.

### Embedded IPv4 addresses

It's possible to embed an IPv4 address in an IPv6 address in some
circumstances. Here we'll just give the notation - the usage is
discussed in
[Chapter 3](https://github.com/becarpenter/book6/tree/main/3.%20Coexistence%20with%20legacy%20IPv4).

An IPv4-mapped IPv6 address is a way to represent an IPv4 address as if
it was an IPv6 address, e.g.

```
 96 bit
 prefix -- IPv4 ---
 |    | |         |
 ::ffff:192.0.2.123
```

That is, the prefix at full length would be `0:0:0:0:0:ffff::/96`.

(Note that `::ffff::/96` would be ambiguous. Only one '::' is allowed.)

In particular, this form of address can be used to make the IPv6 socket
interface handle an IPv4 address (see
[RFC 4038](https://www.rfc-editor.org/info/rfc4038)).

### Multicast addresses

IPv6 multicast address are all under the `ff00::/8` prefix, i.e. they
start with 0xff. The next 8 bits have special meanings, so 112 bits are
left to specify a particular multicast group. The special meanings are
well explained in Section 2.7 of
[RFC 4291](http://www.rfc-editor.org/info/rfc4291), so this is not
repeated here. Some multicast addresses are predefined; for example
`ff02::1` is the link-local "all nodes" address that every IPv6 node
must listen to, and `ff02::2` is the link-local "all routers" address
that every IPv6 router must listen to.

All the officially assigned multicast addresses may found at
[IANA](https://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xhtml#link-local).

### Literal addresses in web browsers

Browsers can recognize a literal IPv6 address instead of a host name,
but the address must be enclosed in square brackets, e.g.:

```
   https://[2001:db8:4006:80b:a1b3:6d7a:3f65:dd13]
```

Of course, literal addresses should only be used for diagnostic or
testing purposes, and will normally be cut-and-pasted rather than being
typed in by hand.

### Some addresses are special

Special-purpose IPv6 addresses and their registry are described in
[RFC 6890](https://www.rfc-editor.org/info/rfc6890).

You may have noticed that many examples above use the prefix
`2001:db8::/32`. That prefix is reserved for documentation and should
never appear on the real Internet
\[[RFC3849](https://www.rfc-editor.org/info/rfc3849)\]. For documenting
examples that need a prefix shorter than /32, the prefix `3fff::/20` has
been reserved \[[RFC9637](https://www.rfc-editor.org/info/rfc9637)\].

Another special case worth mentioning is the _discard prefix_
`0100::/64`; a packet sent to any address in this prefix will be dropped
\[[RFC6666](https://www.rfc-editor.org/info/rfc6666)\].

### Obsolete address types

- A mapping of some OSI addresses into IPv6 addresses, and of arbitrary
  OSI addresses into IPv6 destination options, was made obsolete by
  [RFC 4048](https://www.rfc-editor.org/info/rfc4048).

- A format known as "Top Level Aggregator (TLA)" was made obsolete by
  [RFC 3587](https://www.rfc-editor.org/info/rfc3587).

- A format known as "site-local" addresses was made obsolete by
  [RFC 3879](https://www.rfc-editor.org/info/rfc3879).

- A format known as "IPv4-Compatible IPv6" addresses was made obsolete
  by [RFC 4291](https://www.rfc-editor.org/info/rfc4291).

- Address prefixes previously allocated for special use are mentioned in
  the
  [unicast address registry](https://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xhtml).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Packet%20Format.md) [<ins>Next</ins>](Layer%202%20functions.md) [<ins>Top</ins>](02.%20IPv6%20Basic%20Technology.md)

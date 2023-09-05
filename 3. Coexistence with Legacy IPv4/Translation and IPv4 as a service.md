## Translation and IPv4 as a service

When an operator wants to reduce infrastructure costs by running a
single protocol, IPv6, instead of a dual stack, the strategic approach
is to minimize IPv4 presence in the network. Unfortunately, some
resources are available only on IPv4 and some client applications may
*require* IPv4. Hence, a pure IPv6-only environment is unrealistic for
the foreseeable future. In some situations, tunneling (as described
above) is sufficient, but typically translation between IPv6 and IPv4 is
unavoidable. Especially, when providing IPv4 as a Service (IPv4aaS), a
typical scenario will:

1. Let IPv6 native traffic flow directly between the client and the
   server.
1. Translate the traffic of local IPv6 clients to remote IPv4-only
   servers, using a centralized NAT64 device.
1. Encapsulate literal IPv4 address requests into IPv6 on the client
   then decapsulate and translate it on the centralized NAT to access
   the IPv4 server.

Because of this, it is essentially impossible to separate the discussion
of translation techniques from the discussion of IPv4 as a service.

### Terminology

- SIIT (Stateless IP/ICMP Translation Algorithm). This is also known
  simply as "IP/ICMP Translation Algorithm"
  \[[RFC7915](https://www.rfc-editor.org/info/rfc7915)\],
  \[[RFC6144](https://www.rfc-editor.org/info/rfc6144)\]. It translates
  IPv4 packets to IPv6 format and the opposite. Note that translation is
  limited to basic functionality, and does not translate any IPv4
  options or any IPv6 extension headers except the Fragment Header.
  Technically the mechanism is stateless (i.e., it relies on no stored
  information) but in practice it is used as part of stateful
  mechanisms.

- NAT64 refers to address translation between IPv6 clients and IPv4
  servers, using the SIIT mechanism.

  - [RFC6146](https://www.rfc-editor.org/info/rfc6146) defines
    _stateful_ NAT64, which (like IPv4 NAT) includes port translation
    and supports two-way transport sessions.
  - DNS64 \[[RFC6147](https://www.rfc-editor.org/info/rfc6147)\]
    supports DNS extensions for clients of stateful NAT64.
  - PREF64 refers to the IPv6 prefix used "outside" the NAT64
    translator. [RFC8781](https://www.rfc-editor.org/info/rfc8781)
    and [RFC8880](https://www.rfc-editor.org/info/rfc8880)
    are mechanisms by which a host can learn the PREF64 in use.

- 464XLAT (Combination of Stateful and Stateless Translation)
  \[[RFC6877](https://www.rfc-editor.org/info/rfc6877)\] is SIIT plus
  address translation *from* IPv4 clients to IPv6 transport and *back
  to* IPv4 servers. This is used for IPv4 traffic to cross an
  IPv6-only network.

  - CLAT is the client side translator in 464XLAT. It implements stateless NAT46 (SIIT) translation.
  - PLAT is the provider side translator in 464XLAT. It is nothing else than a stateful NAT64 gateway.
  - This is the only well-defined model for NAT464 translation.

- The final two items have nothing to do with IPv6/IPv4 co-existence but
  are included here for completeness:

  - NPTv6 (IPv6-to-IPv6 Network Prefix Translation) is an *experimental*
    technique \[[RFC6296](https://www.rfc-editor.org/info/rfc6296)\]
    whose applicability is debated.

  - NAT66 is not defined by the IETF and, given the vast supply of IPv6
    addresses, is not generally considered useful enough to overcome its
    disadvantages, which it shares with classical IPv4 NAT
    \[[RFC5902](https://www.rfc-editor.org/info/rfc5902)\].

### Further details of IPv4 as a service

Point 2 listed above evidently needs stateful NAT64
\[[RFC 6146](https://www.rfc-editor.org/info/rfc6146)\].

Additionally, the client could be triggered to start a cross-protocol
connection. For this, the client should be told that the server is
available on the IPv6 Internet. DNS64
\[[RFC 6147](https://www.rfc-editor.org/info/rfc6147)\] can do this on
the ISP side. It can synthesize an IPv6 address from an IPv4 address, by
adding a particular static prefix. When the client asks for
`www.example.net` (which only has an A record in the global DNS), DNS64
will synthesize and return an AAAA record. Deployment of DNS64 involves
complications and is not necessary in the presence of IPv4-as-a-service.

Point 3 above may be implemented (in addition to points 1 and 2) by
various technologies:

- 464XLAT (Combination of Stateful and Stateless Translation)
  \[[RFC 6877](https://www.rfc-editor.org/info/rfc6877)\]
- DS-Lite (Dual-Stack Lite)
  \[[RFC 6333](https://www.rfc-editor.org/info/rfc6333)\]
- lw4o6 (Lightweight 4over6)
  \[[RFC 7596](https://www.rfc-editor.org/info/rfc7596)\]
- MAP E (Mapping of Address and Port with Encapsulation)
  \[[RFC 7597](https://www.rfc-editor.org/info/rfc7597)\]
- MAP T (Mapping of Address and Port using Translation)
  \[[RFC 7599](https://www.rfc-editor.org/info/rfc7599)\].

[RFC 9313](https://www.rfc-editor.org/info/rfc9313) has a good overview
and comparison of these technologies.

The following figure illustrates such a scenario.
<img src="./vasilenko-IPv4aaS.svg" alt="User devices connected to Internet via IPv6 infrastructure" width="auto" height="auto"/>

- 464XLAT is the widely preferred translation technology now because it
  has a natural synergy with NAT64 (which is highly desirable by itself)
  and because it is the only solution supported on mobile devices. The
  centralized NAT64 engine is called PLAT, and is the same
  \[[RFC 6146](https://www.rfc-editor.org/info/rfc6146)\] as for
  ordinary NAT64. The client side is called CLAT, and is typically a
  stateless NAT46 translation
  \[[RFC 7915](https://www.rfc-editor.org/info/rfc7915)\]. A good
  analysis of deployment considerations is in
  [RFC8683](https://www.rfc-editor.org/info/rfc8683), from which an
  operator might conclude *not* to implement DNS64, since IPv4 clients
  can simply use the normal DNS A records and the IPv4 service as if it
  was native.

- DS-Lite was the most popular technology for a considerable period of
  time.

- Lw6o4 has not gained significant market adoption.

- Technically, MAP-E and MAP-T are stateless with significant related
  advantages: no need for logs, possible to implement on routers. But
  MAP needs a rather big IPv4 address space to be reserved for all
  clients (even when disconnected) and MAP is not available by default
  on the majority of Mobile OSes. As a result, MAP has a small market
  share.

### Further details of NPTv6

Network Prefix Translation (NPTv6)
\[[RFC 6296](https://www.rfc-editor.org/info/rfc6296)\] is a special
technology available only in IPv6. It exchanges prefixes between
“inside” (private network) and “outside” (public network) of the
translation engine and modifies the IID. The IID is changed so as
preserve the transport layer checksum despite the prefix change. Hence,
it is transparent for all transport layer protocols. In principle it
would, for example, allow a site using ULA addresses
\[[2. Addresses](../2.%20IPv6%20Basic%20Technology/Addresses.md)\] to
communicate with global IPv6 addresses, but with some of the
disadvantages of classical IPv4 NAT. The principal difference between
NPTv6 and classical NAT is that it permits connection initiation in both
directions. However, it is not fully transparent for applications that
embed IP addresses at high layers (so-called “referrals”). Hence, it
cannot be considered end-to-end transparent.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Tunnels.md) [<ins>Next</ins>](Obsolete%20techniques.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

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
  \[[RFC7915](https://www.rfc-editor.org/info/rfc7915),
  [RFC 6144](https://www.rfc-editor.org/info/rfc6144)\]. It translates
  IPv4 packets to IPv6 format and the opposite. Note that translation is
  limited to basic functionality, and does not translate any IPv4
  options or any IPv6 extension headers except the Fragment Header.
  Technically the mechanism is stateless (i.e., it relies on no stored
  information) but in practice it is used as part of stateful
  mechanisms.

- NAT64 refers to address translation between IPv6 clients and IPv4
  servers, using the SIIT mechanism.

  - [RFC 6146](https://www.rfc-editor.org/info/rfc6146) defines
    _stateful_ NAT64, which (like IPv4 NAT) includes port translation
    and supports two-way transport sessions.
  - DNS64 \[[RFC6147](https://www.rfc-editor.org/info/rfc6147)\]
    supports DNS extensions for clients of stateful NAT64.
  - PREF64 refers to the IPv6 prefix used "outside" the NAT64
    translator. [RFC 8781](https://www.rfc-editor.org/info/rfc8781) and
    [RFC 8880](https://www.rfc-editor.org/info/rfc8880) are mechanisms
    by which a host can learn the PREF64 in use.

- 464XLAT (Combination of Stateful and Stateless Translation)
  \[[RFC6877](https://www.rfc-editor.org/info/rfc6877)\] is SIIT plus
  address translation *from* IPv4 clients to IPv6 transport and *back
  to* IPv4 servers. This is used for IPv4 traffic to cross an IPv6-only
  network.

  - CLAT is the client side translator in 464XLAT. It implements
    stateless NAT46 (SIIT) translation.
  - PLAT is the provider side translator in 464XLAT. It is nothing else
    than a stateful NAT64 gateway.
  - This is the only well-defined model for NAT464 translation.

- The final two items have nothing to do with IPv6/IPv4 co-existence but
  are included here for completeness:

  - NPTv6 (IPv6-to-IPv6 Network Prefix Translation) is an *experimental*
    technique \[[RFC6296](https://www.rfc-editor.org/info/rfc6296)\]
    whose applicability is debated.

  - NAT66 is not defined by the IETF and, given the vast supply of IPv6
    addresses, is not generally considered useful enough to overcome its
    disadvantages, which it shares with classical IPv4 NAT
    \[[RFC5902](https://www.rfc-editor.org/info/rfc5902)\]. Like IPv4
    NAT, it may be implemented with support of port translation (i.e.,
    NAPT66), but as there is no shortage of IPv6 addresses, port
    translation is unnecessary.

### Further details of IPv4 as a service

Point 2 listed above evidently needs stateful NAT64
\[[RFC6146](https://www.rfc-editor.org/info/rfc6146)\].

Additionally, the client could be triggered to start a cross-protocol
connection. For this, the client should be told that the server is
available on the IPv6 Internet. DNS64
\[[RFC6147](https://www.rfc-editor.org/info/rfc6147)\] can do this on
the ISP side. It can synthesize an IPv6 address from an IPv4 address, by
adding a particular static prefix. When the client asks for
`www.example.net` (which only has an A record in the global DNS), DNS64
will synthesize and return an AAAA record. Deployment of DNS64 involves
complications and is not necessary in the presence of IPv4-as-a-service.

Point 3 above may be implemented (in addition to points 1 and 2) by
various technologies:

- 464XLAT (Combination of Stateful and Stateless Translation)
  \[[RFC6877](https://www.rfc-editor.org/info/rfc6877)\]
- DS-Lite (Dual-Stack Lite)
  \[[RFC6333](https://www.rfc-editor.org/info/rfc6333)\]
- lw4o6 (Lightweight 4over6)
  \[[RFC7596](https://www.rfc-editor.org/info/rfc7596)\]
- MAP E (Mapping of Address and Port with Encapsulation)
  \[[RFC7597](https://www.rfc-editor.org/info/rfc7597)\]
- MAP T (Mapping of Address and Port using Translation)
  \[[RFC7599](https://www.rfc-editor.org/info/rfc7599)\].

[RFC 9313](https://www.rfc-editor.org/info/rfc9313) has a good overview
and comparison of these technologies.

The following figure illustrates such a scenario.
<img src="./vasilenko-IPv4aaS.png" alt="User devices connected to Internet via IPv6 infrastructure" width="auto" height="auto"/>

- 464XLAT is the widely preferred translation technology now because it
  has a natural synergy with NAT64 (which is highly desirable by itself)
  and because it is the only solution supported on mobile devices. The
  centralized NAT64 engine is called PLAT, and is the same
  \[[RFC6146](https://www.rfc-editor.org/info/rfc6146)\] as for ordinary
  NAT64. The client side is called CLAT, and is typically a stateless
  NAT46 translation
  \[[RFC7915](https://www.rfc-editor.org/info/rfc7915)\]. A good
  analysis of deployment considerations is in
  [RFC 8683](https://www.rfc-editor.org/info/rfc8683), from which an
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

### IPv4 as a service for mobile devices

The diagram above covers IPv4aaS for a network. A special case is
IPv4aaS for a mobile device, especially when the device has only been
provided with a single /64 prefix, as is the case in most 3GPP
deployments. In this case, 464XLAT is the only available solution, and
as described in Section 6.3 of
[RFC 6877](https://www.rfc-editor.org/info/rfc6877), the CLAT will use a
specific address from that /64 prefix.

### Further details of NPTv6

Network Prefix Translation (NPTv6)
\[[RFC6296](https://www.rfc-editor.org/info/rfc6296)\] is a special
technology available only in IPv6. It exchanges prefixes between
“inside” (private network) and “outside” (public network) of the
translation engine and modifies the IID. The IID is changed so as
preserve the transport layer checksum despite the prefix change. Hence,
it is transparent for all transport layer protocols. In principle it
would, for example, allow a site using ULA addresses
\[[2. Addresses](../2.%20IPv6%20Basic%20Technology/Addresses.md)\] to
communicate with global IPv6 addresses, but with some of the
disadvantages of classical IPv4 NAT, sometimes referred to as 1:1 NAT,
and not to be confused with masquerading address translation. The
principal difference between NPTv6 and classical NAT is that it permits
connection initiation in both directions. However, it is not fully
transparent for applications that embed IP addresses at high layers
(so-called “referrals”). Hence, it cannot be considered end-to-end
transparent.

A particular difficulty is that SIP (Session Initiation Protocol for IP
telephony) will not work behind NPTv6 without the support of a proxy
mechanism \[[RFC6314](https://www.rfc-editor.org/info/rfc6314)\].

As stated above, NPTv6 is outlined in
[RFC 6296](https://www.rfc-editor.org/info/rfc6296); however, although
there is significant commercial support, it should be noted that the RFC
is experimental as of the time of this writing, so it is not considered
standards track.

It goes without saying that NPTv6 is _never_ justified by a shortage of
IPv6 addresses. Nevertheless, while there is controversy about breaking
end-to-end address transparency in IPv6, there are valid use cases for
such architectures, and breaking the end-to-end model is more of an
unfortunate side effect than a feature of such tools. Some details on
the "breakage" caused by NPTv6, and a comparison with classical NAT, are
given in
[Section 5 of RFC 6296](https://www.rfc-editor.org/rfc/rfc6296.html#section-5).

In large scale deployments of wide area architectures, NPTv6 does enable
some compelling use cases which enable diversity in security platforms
such as stateful unified threat management devices (UTMs). These are
positioned in geographically and topologically diverse locations, but
require flexibility of _external_ layer 3 addressing to support flow
identification. Using NPTv6 to perform re-mapping of addressing allows
inspection engines to maintain the flow symmetry that is required for
stateful deep packet inspection engines to operate, as asymmetry will
cause them to mark all flows as incomplete. It is in this model that it
can be GUA to GUA, and this is a valid, supportable, and definitely
production deployed architecture.

In smaller deployments, NPTv6 can be leveraged to create stable
addressing inside a network that may be too small for PI address space,
but too large to operate without service provider diversity. In this
model, such as an SD-WAN deployment, a GUA or ULA prefix may be
deployed, delegated by a home office, other IT governance body, or a
local administrator, and mapped to one or more PA prefixes provided by
lower cost commercial internet services. This allows for internal
addressing to be stable, while providing a more robust connectivity
model, and the ability to more quickly switch providers if required by
leveraging dynamic addressing externally mapped to stable addressing
internally. This model more closely aligns with the current IPv4
architectures pervasively deployed nearly everywhere with stable
internal IPv4 addressing masqueraded to one or more PA addresses
provided by an upstream ISP.

### Further details on NAT66

NAT66 is currently a non-standards based mechanism for statefully
translating one or more IPv6 addresses to one or more other IPv6
addresses. When port translation is also provided (as is very common for
IPv4 NAT), the term NAPT66 may also be used.

It goes without saying that NAT66 is _never_ justified by a general
shortage of IPv6 addresses. Like NPTv6, NAT66 should be used only when
necessary or required. Moreover, is is also very important to understand
that the intent of these tools is to translate, hence the names. They
may play a part in compliance requirements, but they are - at their core
\- translation tools and not security mechanisms. Address translation is
often deployed alongside stateful packet filtering, but the two are, in
actuality, exclusive toolkits. That is to say, they are not tied to each
other, and should be considered distinct - address translation is not a
security tool.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Tunnels.md) [<ins>Next</ins>](Obsolete%20techniques.md) [<ins>Top</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

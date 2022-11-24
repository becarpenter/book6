## Translation

*Editor's comment: this section is under active development...*

*Aide-memoire:

- NAT64
    - DNS64
- 464XLAT
    - RFC6877 
    - CLAT
    - PLAT
- NPTv6
- NAT66*

When an operator wants to reduce costs by running a single protocol, IPv6, instead of a dual stack,
the strategic approach is to minimize IPv4 presence in the network. Unfortunately, some resources are available only on IPv4 and some client applications may *require* IPv4. Hence, a pure IPv6-only
environment is unrealistic: translation between IPv6 and IPv4, or tunneling, is unavoidable
for the majority of environments.

The most popular approach is named IPv4 as a Service (IPv4aaS):
-	Let IPv6 native traffic flow directly between the client and the server,
-	Translate by centralized NAT64 the traffic of local IPv6 clients to remote IPv4-only servers,
-	Encapsulate literal IPv4 address requests into IPv6 on the client then decapsulate and translate it on the centralized NAT to access the IPv4 server.

The second point in the approach above evidently needs stateful NAT64 [RFC 6146](https://www.rfc-editor.org/info/rfc6146). Additionally, the client should be pushed to start such a cross-protocol connection. For this, the client should be misled that the server is available on the IPv6 Internet. DNS64 [RFC 6147](https://www.rfc-editor.org/info/rfc6147) is needed on the ISP side to synthesize the IPv6 address out of IPv4 (just adding the static prefix).

The third point in the approach above may be implemented based on five technologies: 464XLAT [RFC 6877](https://www.rfc-editor.org/info/rfc6877), DS-Lite [RFC 6333](https://www.rfc-editor.org/info/rfc6333), lw4o6 [RFC 7596](https://www.rfc-editor.org/info/rfc7596), MAP E/T [RFC 7597](https://www.rfc-editor.org/info/rfc7597)/[RFC 7599](https://www.rfc-editor.org/info/rfc7599).
[RFC 9313](https://www.rfc-editor.org/info/rfc9313) has a good overview and comparison of these technologies.

The following figure illustrates such a scenario.
<img src="./vasilenko-IPv4aaS.svg" width="auto" height="auto"/>

464XLAN is a popular translation technology now because it has a natural synergy with NAT64 (which is highly desirable by itself) and because it is the only solution supported on mobile devices. The centralized NAT64 engine is called PLAT, it is the same [RFC 6146](https://www.rfc-editor.org/info/rfc6146) as for ordinary NAT64. The client side is called CLAT, it is typically a stateless NAT46 translation [RFC 7915](https://www.rfc-editor.org/info/rfc7915).

DS-Lite was the most popular technology for historical reasons.

Lw6o4 has not gained considerable market adoption.

Technically, MAP-E/T is stateless with many related advantages: no need for logs, possible to implement on routers. But MAP needs rather big IPv4 address space to be reserved for all clients (even disconnected) and MAP is not available by default on the majority of Mobile OSes. As a result, MAP has a small market share.

Network Prefix Translation (NPT) [RFC 6296](https://www.rfc-editor.org/info/rfc6296) is a special technology available only in IPv6. It exchanges prefixes between “inside” and “outside” of the engine and modifies algorithmically the IID. IID change is implemented to compensate transport layer checksum change that did happen because of the prefix change. Hence, it is transparent for all transport layer protocols.
The principal difference between NPT and ordinary NAT is that it permits connection initiation in both directions. Albeit, it is not fully transparent for applications that embed IP addresses at high layers (so-called “referrals”). Hence, it may not be considered end-to-end transparent.

NAT66 breaks end-to-end transparency which is considered the primary IPv6 technical advantage over IPv4. IAB has thoroughly discussed many NAT66 problems in [RFC 5902](https://www.rfc-editor.org/info/rfc5902) and then decided not to standardize NAT66. It is in general the IETF consensus supported by the majority of members.

*Editorial note: we need to change the language here to avoid controversy.*


<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Tunnels.md) [<ins>Next</ins>](Obsolete%20techniques.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

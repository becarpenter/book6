## Dual stack scenarios

We must distinguish the original model of dual stack deployment from the new concept of presenting a dual stack to the upper layer protocols while providing IPv4 as a *service* over an IPv6 infrastructure.

### Original dual stack model

Dual-Stack was originally described (along with basic tunneling) in [RFC4213](https://www.rfc-editor.org/rfc/rfc4213). In 2020, it appeared to be the most widely deployed IPv6 solution (about 50%, see the statistics reported in [ETSI-IP6-WhitePaper](https://www.etsi.org/images/files/ETSIWhitePapers/etsi_WP35_IPv6_Best_Practices_Benefits_Transition_Challenges_and_the_Way_Forward.pdf)).

In a classical dual stack deployment, packets on the link are either native IPv6 or native IPv4. All routers support IPv6 and IPv4 simultaneously, with separate routing tables: this is known as "ships in the night".

~~~
Ships that pass in the night, and speak [to] each other in passing,
only a signal shown, and a distant voice in the darkness
  --  Henry Wadsworth Longfellow, 1863
~~~

Today, the core of the Internet - all the major international transit providers and all major Internet Exchange Points - support dual stack routing. So do many local ISPs.

Also, all hosts in a dual stack network should support IPv6 and IPv4 simultaneously, with IPv6 preferred. Such a deployment can tolerate the presence of legacy IPv4-only hosts and applications, and can reach external IPv4-only services, with no special arrangements. An essential part of this model is that applications using the network see a version of the socket API that intrinsically supports both IPv4 and IPv6. Thus, \[[RFC3542](https://www.rfc-editor.org/info/rfc3542)] introduced a dual-stack API, including the important ```getaddrinfo()``` ("get address information") function, which has since been adopted by both POSIX and Windows operating systems. 

[RFC8305](https://www.rfc-editor.org/info/rfc8305) explains the "Happy Eyeballs" technique for applications seeking to optimize dual-stack performance.
   
With Dual-Stack, IPv6 can be introduced together with other network upgrades and many parts of network management and Information Technology (IT) systems can still work in IPv4. As a matter of fact, IPv4 reachability can be provided for a long time and most Internet Service Providers (ISPs) are leveraging Carrier-Grade NAT (CGN, [RFC6888](https://www.rfc-editor.org/info/rfc6888)) to extend the life of IPv4. However, large ISPs have discovered the scaling limits and operational costs of CGN.
   
Although Dual-Stack provides advantages in the initial phase of deployment, it has some disadvantages in the long run, like the duplication of network resources and states. It also requires more IPv4 addresses, thus increasing both Capital Expenses (CAPEX) and Operating Expenses (OPEX). To be clear, a network (whether a home network or an office network) can today work very smoothly with every host having both an IPv4 address and an IPv6 address, and using whichever works best for a particular application. 

### The need for IPv4 as a service

Globally unique IPv4 addresses are now scarce and have signifcant commercial value. Indeed, even if private IPv4 addresses are used with CGN, global IPv4 addresses for the CGN systems must be paid for by somebody.
   
For this reason, when IPv6 usage exceeds a certain threshold, it may be advantageous to start a transition to a next phase and move to a more advanced IPv6 deployment, also referred to as IPv6-only. To be clear, that does not mean removing access to IPv4-only resources. Some method of access to IPv4 resources must be retained, as the primary network infrastructure is switched from a dual stack. In effect the *application layer* in a host will still see a dual stack environment, even if the packets on the link are no longer a mixture of native IPv6 and native IPv4.

Such solutions are known as "IPv4 as a Service" (IPv4aaS) and can be used to ensure IPv4 support and coexistence when starting the IPv6-only transition for the infrastructure. This can be a complex decision. As mentioned in [a recent draft](https://datatracker.ietf.org/doc/draft-ietf-v6ops-ipv6-deployment/) IPv6-only is generally associated with a scope, e.g. IPv6-only overlay or IPv6-only underlay.

"IPv6-only overlay" denotes that the overlay tunnel between the end points of a network domain is based only on IPv6. IPv6-only overlay in a fixed network means that IPv4 is encapsulated in IPv6 (or translated) at least between the interfaces of the Provider Edge (PE) nodes and Customer Edge (CE) node (or the Broadband Network Gateway (BNG)). As further mentioned in [Tunnels](Tunnels.md), tunneling provides a way to use an existing IPv4 infrastructure to carry IPv6 traffic. There are also translation options described in \[[Translation](Translation.md)]. This approach with IPv6-only overlay helps to maintain compatibility with the existing base of IPv4, but it is not a long-term solution

"IPv6-only underlay" relates to the specific domain, such as IPv6-only access network or IPv6-only backbone network, and means that IPv6 is the network protocol for all traffic delivery. Both the control and data planes are IPv6-based. For example, IPv6-only underlay in fixed network means that the underlay network protocol is only IPv6 between any Provider Edge (PE) nodes.
   
To ensure IPv4 support, the concept of IPv4aaS is introduced and means that IPv4 connection is provided by means of a coexistence mechanism, therefore there is a combination of encapsulation/translation + IPv6-only underlay + decapsulation/translation. IPv4aaS offers Dual-Stack service to users and allows an ISP to run IPv6-only in the network, typically the access network. Some network operators already started this process, as in the case of [T-Mobile US](https://pc.nanog.org/static/published/meetings/NANOG73/1645/20180625_Lagerholm_T-Mobile_S_Journey_To_v1.pdf), [Reliance Jio](https://datatracker.ietf.org/meeting/109/materials/slides-109-v6ops-ipv6-only-adoption-challenges-and-standardization-requirements-03) and [EE](https://indico.uknof.org.uk/event/38/contributions/489/attachments/612/736/Nick_Heatley_EE_IPv6_UKNOF_20170119.pdf).
   
[RFC9313](https://www.rfc-editor.org/rfc/rfc9313) compares the merits of the most common IPv6 transition solutions, i.e. 464XLAT \[[RFC6877](https://www.rfc-editor.org/rfc/rfc6877)], DS-lite \[[RFC6333](https://www.rfc-editor.org/rfc/rfc6333)], Lightweight 4over6 (lw4o6) \[[RFC7596](https://www.rfc-editor.org/rfc/rfc7596)], MAP-E \[[RFC7597](https://www.rfc-editor.org/rfc/rfc7597)], and MAP-T \[[RFC7599](https://www.rfc-editor.org/rfc/rfc7599)].

A framework for carriers is proposed in a current draft [draft-xie-v6ops-framework-md-ipv6only-underlay](https://datatracker.ietf.org/doc/draft-xie-v6ops-framework-md-ipv6only-underlay/). The reader will notice that the solutions most commonly adopted today, such as this one, exploit both the use of tunnels (IPv4 carried over IPv6) and translation (IPv4 re-encoded as IPv6). The following two sections separate out these two techniques.


<!-- Link lines generated automatically; do not delete -->
### [<ins>Next</ins>](Tunnels.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

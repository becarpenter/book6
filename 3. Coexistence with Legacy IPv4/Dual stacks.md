## Dual stacks

Dual-Stack [RFC4213](https://www.rfc-editor.org/rfc/rfc4213) appears to be currently the most widely deployed IPv6 solution (about 50%, see the statistics reported in [ETSI-IP6-WhitePaper](https://www.etsi.org/images/files/ETSIWhitePapers/etsi_WP35_IPv6_Best_Practices_Benefits_Transition_Challenges_and_the_Way_Forward.pdf)). 
   
With Dual-Stack, IPv6 can be introduced together with other network upgrades and many parts of network management and Information Technology (IT) systems can still work in IPv4. As a matter of fact, IPv4 reachability can be provided for a long time and most Internet Service Providers (ISPs) are leveraging Carrier-Grade NAT (CGN) to extend the life of IPv4.
   
Although Dual-Stack may provide advantages in the initial phase, it has few disadvantages in the long run, like the duplication of the network resources and states. It also requires more IPv4 addresses, thus increasing both Capital Expenses (CAPEX) and Operating Expenses (OPEX). Indeed, even if private addresses are used with CGN, it is necessary an investment in the CGN systems.
   
For this reason, when IPv6 usage exceeds certain threshold, it may be advantageous to switch to start a transition to a next phase and move to a more advanced IPv6 deployment, also referred to as IPv6-only. As mentioned in [I-D.ietf-v6ops-ipv6-deployment](https://datatracker.ietf.org/doc/draft-ietf-v6ops-ipv6-deployment/) IPv6-only is generally associated with a scope, e.g.  IPv6-only overlay or IPv6-only underlay.
   
The IPv6-only overlay denotes that the overlay tunnel between the end points of a network domain is based only on IPv6. IPv6-only overlay in fixed network means that the encapsulation is only IPv6 between the interfaces of the Provider Edge (PE) nodes or between the WAN interface of the Customer Edge (CE) node and the Broadband Network Gateway (BNG) interface. 
   
To ensure IPv4 support, the concept of IPv4 as a Service (IPv4aaS) is introduced and means that IPv4 connection is provided by means of transition mechanism, therefore there is a combination of encapsulation/translation + IPv6-only overlay + decapsulation/translation. IPv4aaS offers Dual-Stack service to users and allows an ISP to run IPv6-only in the network (typically, the access network). Some network operators already started this process, as in the case of [T-Mobile US](https://pc.nanog.org/static/published/meetings/NANOG73/1645/20180625_Lagerholm_T-Mobile_S_Journey_To_v1.pdf), [Reliance Jio](https://datatracker.ietf.org/meeting/109/materials/slides-109-v6ops-ipv6-only-adoption-challenges-and-standardization-requirements-03) and [EE](https://indico.uknof.org.uk/event/38/contributions/489/attachments/612/736/Nick_Heatley_EE_IPv6_UKNOF_20170119.pdf).
   
[I-D.ietf-v6ops-transition-comparison](https://datatracker.ietf.org/doc/draft-ietf-v6ops-transition-comparison/) compares the merits of the most common IPv6 transition solutions, i.e. 464XLAT [RFC6877](https://www.rfc-editor.org/rfc/rfc6877), DS-lite [RFC6333](https://www.rfc-editor.org/rfc/rfc6333), Lightweight 4over6 (lw4o6) [RFC7596](https://www.rfc-editor.org/rfc/rfc7596), MAP-E [RFC7597](https://www.rfc-editor.org/rfc/rfc7597), and MAP-T [RFC7599](https://www.rfc-editor.org/rfc/rfc7599).   
   
IPv6-only underlay network relates to the specific domain, such as IPv6-only access network or IPv6-only backbone network, and means that IPv6 is the network protocol for all traffic delivery. Both the control and data planes are IPv6-based. For example, IPv6-only underlay in fixed network means that the underlay network protocol is only IPv6 between any Provider Edge (PE) nodes.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Next</ins>](Tunnels.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

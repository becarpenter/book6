## Topology hiding

There are various operational contexts in which an operator needs to hide a network's topology, equipment, and hosts from outsiders. Since IPv6 promotes end-to-end addressing, the question arises of how to achieve topology hiding or obfuscation in the absence of network address translation (NAT).

One important context for this is networks that must conform to standards such as Payment Card Industry
Data Security Standard Requirements (PCI-DSS), issued by the [PCI Security Standards Council](https://www.pcisecuritystandards.org). (This standard can be [downloaded](https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0.pdf) free of charge, but beware that you must agree to a license in order to do so.) PCI-DSS requires an enterprise that stores certain types of customer data to do so on servers that are effectively isolated from the Internet and undiscoverable from outside the enterprise. Yet these servers might also be offering Web services to clients anywhere in the Internet. A common solution to this dilemma for IPv4 has two parts:

1. A "demilitarized zone" (DMZ) between the Internet and the core of the enterprise network.

2. When a server in the core communicates with a client elsewhere in the Internet, the requirement to hide the server is commonly satisfied by IPv4 NAT between the server and the DMZ. 

It goes without saying that such traffic will flow through a firewall (which PCI-DSS refers to as a Network Security Device or NSD). The question is how should such a system obscure the server's regular IPv6 address as effectively as NAT obscures its IPv4 address. Note that PCI-DSS (version 4, March 2022) does not require NAT, although it is mentioned as a solution for IPv4. For IPv6, it suggests using temporary addresses \[[RFC8981](https://www.rfc-editor.org/info/rfc8981)] for outgoing sessions (although it cites an obsoleted RFC). Placing system components behind proxy servers is also suggested, and it seems probable that large installations will do this anyway to support load balancing \[[RFC7098](https://www.rfc-editor.org/info/rfc7098)]. Proxy servers and load balancers will intrinsically hide the core topology from attackers.

Other aspects of topology hiding were discussed in [RFC4864](https://www.rfc-editor.org/info/rfc4864), but that document is significantly out of date.

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Filtering.md) [<ins>Chapter Contents</ins>](4.%20Security.md)

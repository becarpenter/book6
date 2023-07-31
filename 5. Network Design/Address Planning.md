## Address Planning

As you may wonder in IPv6 networks all nodes may have globally unique addresses. All networks will be given at least a /64 global prefix to operate. As for carriers, it should deliver a longer prefix to subscribers, so that they can have multiple /64 subnets within their organizations or home environments. Even a home customer can have a public network prefix to be split into smaller networks, which is a paradigm shift from “hiding behind NAT" on a few public IPv4 addresses. 
Back to IPv6 networks, it is often necessary to manage received prefixes, even if it is done automatically by a CE router. Likewise, network operators receive large address blocks from the RIRs and must plan their address distribution in order to handle address blocks assigned to customers or their own infrastructure.
For instance, we can start with a network operator. Consider an carrier called “ISP” that received the prefix “2001:db8::/32”. It is necessary to separate address blocks asignated for home customers, corporate customers and for ISP's own infrastructure. 
First, let's see what space is available for planning:
```
 Global ID -Subnets- -- Interface IDs --
| 32 bits | 32 bits |   64 bits         |
 2001:0db8:0000:0000:0000:0000:0000:0000
```
The first 32 bits will remain unchanged, of course, and the last 64 bits part will always belong to the ending subnet nodes. It leaves us the 32 bits between them to work with. Keep in mind that there is no concern about exhaustion of IPv6 addresses(or prefixes), see that this single assignment for a autonomous system (ISP) gives a entire IPv4 Internet address space to work with. And this is not about unique addresses, but /64 network prefixes each. As a analogy, a /64 prefix would be the equivalent of leasing a public IPv4 address to a single network or subscriber. In this way, on IPv6 planning we prize for organizigation and clearer management instead of saving as much addresses as possible. On IPv6 networks it makes no sense counting unique addresses, instead, the number of available /64 prefixes. Think of a /64 prefix as a standard unit that fits all networks sizes. 
Remember that 32-bit embodies 4 billion /64 networks, so there is room for good planning and management as there will be no addresses shortage. A good addressing plan should always have room for future expansion and favor network aggregation and management. For this reason, in the following example, we will use the technique known as **leftmost**, to guarantee a more balanced distribution on all available space.
Back to example, consider our 32 bits where we can use the first 4(one character) to assign sixteen regions, as 0 to F. A region may be a data center, geographical area or a branching network.



<!-- Link lines generated automatically; do not delete -->

### [<ins>Chapter Contents</ins>](5.%20Network%20Design.md)

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
Back to example, consider our 32 bits where we can use the first 4(one character) to assign sixteen regions, as 0 to F, resulting on a /36 per region. A region may be a data center, geographical area or a branching network.
A. Region A - Main Datacenter
B. Region B - City south
C. Region B - City north
So the first layer of our address plan may look like this:
```
2001:0db8:0000::/36 - Reserved
2001:0db8:1000::/36 - Reserved
2001:0db8:2000::/36 - Reserved
2001:0db8:3000::/36 - Reserved
2001:0db8:4000::/36 - Reserved
2001:0db8:5000::/36 - Reserved
2001:0db8:6000::/36 - Reserved
2001:0db8:7000::/36 - Reserved
2001:0db8:8000::/36 - Reserved
2001:0db8:9000::/36 - Reserved
2001:0db8:A000::/36 - Region A
2001:0db8:B000::/36 - Region B
2001:0db8:C000::/36 - Region C
2001:0db8:D000::/36 - Reserved
2001:0db8:E000::/36 - Reserved
2001:0db8:F000::/36 - Reserved
```
Each region have functional divisions that may earn one or more address blocks. Each division could be for instance:
1. Internal infrastructure
2. Domestic clients
3. Corporate clients
Using the same logic you can split a region's /36 on 16 /40 prefixes, so it is easier to manage. Keep in mind that it is possible to assign more prefixes for each one if necessary. Now let's see the address plan for **Region A** where we have 16 /40 prefixes:
```
2001:0db8:A000::/40 - Corporate clients ---|
2001:0db8:A100::/40 - Corporate clients    |---> 1024 x /48 prefixes
2001:0db8:A200::/40 - Corporate clients    |
2001:0db8:A300::/40 - Corporate clients ---|
2001:0db8:A400::/40 - Internal infrastructure ---> 256 x /48 prefixes for infrastructure
2001:0db8:A500::/40 - Reserved
2001:0db8:A600::/40 - Reserved ---> 768 x /48 prefixes for expansion
2001:0db8:A700::/40 - Reserved
2001:0db8:A800::/40 - Domestic clients ---|
2001:0db8:A900::/40 - Domestic clients    | 2048 x /48 prefixes
2001:0db8:AA00::/40 - Domestic clients    | or
2001:0db8:AB00::/40 - Domestic clients    | 2001:db8:A800::/37
2001:0db8:AC00::/40 - Domestic clients    | or 
2001:0db8:AD00::/40 - Domestic clients    | 2048 x 256 x /56 prefixes
2001:0db8:AE00::/40 - Domestic clients    |
2001:0db8:AF00::/40 - Domestic clients ---|
```
As shown above, we have a good mesure for corporate and home customers, plus a room for expansion, added by a generous /40 just for internal infrastructure. Of course, this can be changed according to needs on each case. For example, increase the number of prefixes for corporate clients, or take some space in infrastructure reserved part, which is very large. Even add another entire /36 block for the same region. If you do the math, the numbers are always very loose so that we can always give preference to address organization, aggregation and good management.

### Client delegations

It is recommended to delegate at least a /48 block to clients. Best practice says that corporate clients always receive at least a /48 prefix and domestic clients receive at least a /56 prefix. Mobile access clients can receive a single /64. See below where 2 prefixes from Region A's /40 block. A /48 assigned to a corporate customer and a /56 to a domestic customer:
1. 2001:0db8:A3CC:0000::/48
   The least four Zeros shows 16 bits given within a /48 prefix, available to address 2^16=65536 /64 subnets.
2. 2001:0db8:ABDD:DD00::/56
   The least two Zeros represents 8 bits given within a /56 prefix available to address 2^8=256 /64 subnets.

See that a single corporate client is up to a virtually unlimited address space and a domestic subscriber may have 256 subnets on a home network.
Once a client leases an address block it has to split it for given subnets inside the network. Lets take that mentioned home customer with the 2001:0db8:ABDD:DD00::/56 prefix and see wht we can do:
```
2001:0db8:ABDD:DD00::/64 ---> Main home subnet
2001:0db8:ABDD:DD01::/64 ---> Wifi subnet
2001:0db8:ABDD:DD02::/64 ---> Wifi Guest subnet
2001:0db8:ABDD:DD(...)::/64 ---> Reserved
2001:0db8:ABDD:DDFE::/64 ---> IoT subnet
2001:0db8:ABDD:DDFF::/64 ---> VoIP subnet
```
ISP customers tipically lease address blocks through **DHCPv6 prefix delegation**. Instead of aqquiring only one Internet facing address, the customer premice router requests for a entire GUA block. Once it have it, the smaller /64 blocks are tipically handled as a prefix pool, where each is assigned to a internal subnet.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Chapter Contents</ins>](5.%20Network%20Design.md)

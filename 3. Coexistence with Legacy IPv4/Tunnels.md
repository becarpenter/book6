## Tunnels

At its simplest, two IPv6 hosts or networks can be joined together via IPv4 with a tunnel, i.e. an arrangement whereby a device at each end acts as a tunnel end-point. Typically such a tunnel connects two IPv6 routers, using a very simple IPv6-in-IPv4 encapsulation described in [RFC4213](https://www.rfc-editor.org/info/rfc4213), using IP Protocol number 41 to tell IPv4 that the payload is IPv6. Conversely, IPv4-in-IPv6 tunnels are also possible, using IPv6 Next Header value 4 to tell IPv6 that the payload is IPv4..

However, such simple encapsulation is rarely needed today, with direct IPv6 transit being widely available. Tunnels are used in numerous co-existence scenarios, some of which we will now describe.

TBD

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Dual%20stacks.md) [<ins>Next</ins>](Translation.md) [<ins>Chapter Contents</ins>](3.%20Coexistence%20with%20Legacy%20IPv4.md)

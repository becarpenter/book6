## Deployment in the home

It is hard to estimate what fraction of home users have IPv6
connectivity on a given date. The
[Google](https://www.google.com/intl/en/ipv6/statistics.html) statistics
are interesting, because they clearly show weekend peaks in IPv6 access
(up to 43% in April 2023), suggesting a quite high level of home and/or
mobile IPv6 connectivity.

Some, but not all, devices on the market for home (or small office) use
support both IPv6 and IPv4. However, older devices only have IPv4. For
this reason, a typical home network today runs a dual stack. Also, a
typical network does not include multiple subnets; the only router
present is at the same time the subnet router and the CE router.
Assuming the ISP supports IPv6, regardless whether it provides native
IPv4 or IPv4 as a service, the router provides a dual stack service on
the LAN. The LAN itself is typically WiFi, possibly bridged to Ethernet.
(Even if the CE router does *not* support IPv6 at all, link-local IPv6
should work.)

As a result, things are fairly simple. Devices such as PCs and printers
can communicate with each other using whatever works -- IPv4, link-local
IPv6, or global IPv6. (For example: a Windows 10 PC installed in 2019
communicates with a Canon inkjet printer installed in 2022, using
link-local IPv6, needing no manual configuration.) Connections to the
Internet will be preferentially established using IPv6 for services that
have a AAAA address in the DNS, or IPv4 otherwise. Such connections may
be optimized by the Happy Eyeballs technique
\[[RFC8305](https://www.rfc-editor.org/info/rfc8305)\]. Most home users
will remain largely ignorant of all this.

The situation becomes more complicated when various home automation
devices are considered, especially if it becomes desirable to split the
home network into separate subnets. Such networks need to be essentially
self-configuring and self-managing, as do "Internet of Things" networks.
These complex topics are out of scope for this book.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Deployment%20by%20carriers.md) [<ins>Next</ins>](Deployment%20in%20the%20enterprise.md) [<ins>Chapter Contents</ins>](8.%20Deployment%20Status.md)

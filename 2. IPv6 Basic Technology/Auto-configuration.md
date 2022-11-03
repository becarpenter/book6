## Auto-configuration

One design goal for IPv6 was that it could be used "out of the box" in an isolated network (referred to in the early 1990s as a "dentist's office" network). Today, of course, this is a less likely scenario if taken literally, but all the same, isolated network segments do indeed arise. For this scenario, IPv6 has an elegant solution: when an IPv6 node first detects an active network interface, it will automatically configure a link-local address on that interface, such as `fe80::a1b3:6d7a:3f65:dd13`. The interface identifier is a pseudo-random 64-bit number, normally fixed for a given interface. (In legacy implementations, it may be derived from the interface's IEEE MAC address, but this method is now deprecated.)

Link-local addresses are usable only for operations on the same link. The most common case is for traffic between a host and its first-hop router. Another likely case is traffic between a host and local printer. There is nothing to stop them being used for any other type of traffic between local nodes, but they are useless *off* the given link and should definitely never appear in DNS.

Further details are given in {{{RFC4862}}}. Also, we have skipped two important issues that will be discussed later: duplicate address detection and *why* the interface-identifier is pseudo-random.

More coming soon...

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](Address%20resolution.md) [<ins>Next</ins>](Managed%20configuration.md) [<ins>Chapter Contents</ins>](2.%20IPv6%20Basic%20Technology.md)
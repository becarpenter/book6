## How a network operations center sees IPv6

This is really the topic of this entire book. In the long term, we
expect that "running an IPv6 network" will be synonymous with "running a
network". IPv6 should not be viewed as an add-on, but as the primary
network protocol. How it coexists and interacts with IPv4 is the subject
of
[Chapter 3](https://github.com/becarpenter/book6/tree/main/3.%20Coexistence%20with%20legacy%20IPv4).
This section gives an overview of how IPv6 looks when viewed from the
NOC, and the rest of the book covers the details.

IPv6 is, at its roots, not fundamentally different from IPv4 - just
different in almost every detail. So the _nature_ of NOC design and
operation is not changed by IPv6, but existing operations and management
tools need to be updated. For example, any configuration databases,
whether home-grown or purchased, must be able to handle IPv6. For
operators, there are many new details to learn. Also, supporting IPv4
and IPv6 simultaneously is obviously more complicated than supporting
only one protocol.

Enterprise networks, carrier networks, and data center networks each
have their own requirements and challenges, with differing geographical
spreads, availability requirements, etc. Various chapters of this book
tackle different aspects of NOC operations:
[5. Network Design](5.%20Network%20Design/5.%20Network%20Design.md),
[6. Management and Operations](6.%20Management%20and%20Operations/6.%20Management%20and%20Operations.md),
[9. Troubleshooting](9.%20Troubleshooting/9.%20Troubleshooting.md). The
[7. Case Studies](7.%20Case%20Studies/7.%20Case%20Studies.md) will also
be relevant to NOCs.

### [<ins>Previous</ins>](How%20an%20application%20programmer%20sees%20IPv6.md) [<ins>Next</ins>](How%20to%20keep%20up%20to%20date.md) [<ins>Top</ins>](1.%20Introduction%20and%20Foreword.md)

## Why version 6

This section is mainly historical.
Cutting a long story short, IPv6 was designed in the early 1990s because
people knew that IPv4 was destined to run out of addresses. But why is
the version number 6?

Some people ask why IPv4 went to version 6, leaping the next number.
This was _not_ related to the programmer's superstition where odd
numbers should be beta releases.
Maybe we should start by asking why IPv4 was version 4. Stated simply,
that was because versions 0 through 3 were assigned in 1977 and 1978
during the evolution from ARPANET to TCP/IP. So version 4
was the next number available for use in the final design
[RFC 791](https://www.rfc-editor.org/info/rfc791). A rather more subtle
explanation is given by the late Danny Cohen, one of the pioneers involved,
at 38 minutes and 26 seconds into the video
[A Brief Prehistory of Voice over IP](http://www.securitytube.net/video/1978).

So why not IPv5? The answer is quite simple. The number 5 in the version
field of the IP header was already assigned for what was called the
Internet Stream Protocol, or ST. It's a bit confusing, but ST, ST-2 and
ST-2+ \[[RFC1819](https://www.rfc-editor.org/info/rfc1819)\] were
designed and proposed as protocols for applications like voice and video
that demand quality of service. As IP datagrams are delivered on a “best
effort” basis, the ST proposals were more like ATM networks, using
stateful relationships, queuing and much more. Each ST flow would hold
connection state and dynamic controls to ensure quality of service. As
we can see in [RFC 1190](https://www.rfc-editor.org/info/rfc1190), the ST
header is completely different from IPv4, except for the very first
field where is the version number 5:

```
 0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  ST=5 | Ver=2 | Pri |T| Bits  |           TotalBytes          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |              HID              |        HeaderChecksum         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               |
   +-                          Timestamp                          -+
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

As ST would be incompatible with IP, the next version number was
assigned to identify its packets. Ever since then, the number 5 was
reserved for ST in the IP version field (layer 3) and protocol number
(layer 4) field. The idea is that routers could differentiate packets or
that IPv4 packets could carry encapsulated ST packets, where the number
5 would show up as an upper layer protocol. Since
[RFC 762](https://www.rfc-editor.org/info/rfc762) we can see number 5
assigned in "protocol numbers":

```
                 ASSIGNED INTERNET PROTOCOL NUMBERS

   In the Internet Protocol (IP) [44] there is a field to identify the
   the next level protocol.  This field is 8 bits in size.  This field
   is called Protocol in the IP header.

   Assigned Internet Protocol Numbers

      Decimal    Octal      Protocol Numbers                  References
      -------    -----      ----------------                  ----------
           0       0         Reserved
           1       1         raw internet datagrams                 [44]
           2       2         TCP-3                                  [36]
           3       3         Gateway-to-Gateway                     [49]
           4       4         Gateway Monitoring Message             [41]
           5       5         ST                                     [45]
           6       6         TCP-4                                  [46]
```

ST protocols never left an experimental phase, but for live experiments
on the early Internet, its own version number was needed. While (as far
as we know) there is no ST in use anywhere in the Internet today, its
version number is still assigned, so it would not make sense for the
__next generation IP__ to carry that number, so it was “skipped”. The
number 6 would only appear a few years later in an “Assigned numbers”
update \[[RFC1700](https://www.rfc-editor.org/info/rfc1700)\], then
named as "Simple Internet Protocol" (SIP). This acronym has
been recycled for the Session Initiation Protocol.

```
Assigned Internet Version Numbers

Decimal   Keyword    Version                            References
-------   -------    -------                            ----------
    0                Reserved                                [JBP]
  1-3                Unassigned                              [JBP]
    4       IP       Internet Protocol                [RFC791,JBP]
    5       ST       ST Datagram Mode                [RFC1190,JWF]
    6       SIP      Simple Internet Protocol                [RH6]
    7       TP/IX    TP/IX: The Next Internet                [RXU]
    8       PIP      The P Internet Protocol                 [PXF]
    9       TUBA     TUBA                                    [RXC]
10-14                Unassigned                              [JBP]
   15                Reserved                                [JBP]
```

Note that IANA had assigned numbers 6 through 9 for the then
“competitors” of what became IPv6. Number 7 was chosen for TP/IX
\[[RFC1475](https://www.rfc-editor.org/info/rfc1475)\], as its designer
expected ST version 2 would use number 6, which did not happen.
But unexpectedly, a different "IPv7" proposal was announced
during the Internet Society's INET conference in Kobe, Japan,
in June 1992, by IAB members. There was no
consensus among IETF engineers at that time about the new protocol, and
some IAB members proposed using ISO/OSI's CLNP - designating it as IPv7
without a formal IANA assignment. This caused some discomfort in the Internet
community and became known in technical circles as the “Kobe incident”.
Numbers 8 and 9 were used by proposals that came to be merged into
IPv6's ultimate design. As the lowest number available after 4, and
already used by the same author's SIP, number 6 was kept for the first
official specification in
[RFC 1883](https://www.rfc-editor.org/info/rfc1883). Therefore, do not
expect IP versions 7 or 8 in the future, nor even 9 that also belongs
to an April fool's day joke
\[[RFC1606](https://www.rfc-editor.org/info/rfc1606)\].

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Acknowledgments.md) [<ins>Chapter Contents</ins>](1.%20Introduction%20and%20Foreword.md)

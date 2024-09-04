## DNS

We assume that the reader has a good general understanding of the Domain
Name System (DNS). Many aspects of the DNS are unaffected by IPv6,
because it was designed on very general principles.

A specific Resource Record type is defined to embed IPv6 addresses: the
AAAA Record \[[RFC3596](https://www.rfc-editor.org/info/rfc3596)\]. This
simply provides a 128 bit IPv6 address in the same way that an A record
provides an IPv4 address. (AAAA is normally pronounced "Quad-A".)

Similarly, reverse lookup is enabled by the `IP6.ARPA` domain. This is
done using 4-byte nibbles respresented as hexadecimal characters, so the
address `2001:db8:4006:80b:a1b3:6d7a:3f65:dd13` will appear as
`3.1.d.d.5.6.f.3.a.7.d.6.3.b.1.a.b.0.8.0.6.0.0.4.8.b.d.0.1.0.0.2.IP6.ARPA.`
Clearly, these entries are for computers, not for humans.

A corollary of defining the AAAA record is that DNS lookups that
*indirectly* cause an A record lookup must also cause a AAAA lookup.
This concerns NS, SRV and MX lookups.

This change also affects API calls that involve the DNS. The old
`gethostbyname()` and `gethostbyaddr()` calls are **OBSOLETE** and
should no longer be used. They are replaced by `getaddrinfo()` and
`getnameinfo()`, which handle IPv6 as well as IPv4. In particular,
`getaddrinfo()` provides the programmer with a list of both IPv6 and
IPv4 addresses, and it is the programmer's job to decide which one to
use. The order in which addresses are presented to the programmer is
determined by a local configuration table on the host, in a way
described by [RFC 6724](https://www.rfc-editor.org/info/rfc6724).
Unfortunately the standard DHCPv6 mechanism for remote configuration of
this table \[[RFC7078](https://www.rfc-editor.org/info/rfc7078)\] is not
widely used. Operators need to be aware of this complexity when
attempting to cause users to favor IPv6 over IPv4 (or the converse).

Apart from this, in an ideal world DNS for IPv6 should not cause extra
operational issues. However, in practice, there are some matters of
concern:

- As noted in
  [2. Managed configuration](../2.%20IPv6%20Basic%20Technology/Managed%20configuration.md),
  the DNS server for a subnet must be announced by a Router
  Advertisement even if DHCPv6 is in use.

- DNS IPv6 Transport Operational Guidelines are documented in
  [BCP 91](https://www.rfc-editor.org/info/bcp91).

- Considerations for Reverse DNS in IPv6 for Internet Service Providers
  are documented in [RFC 8501](https://www.rfc-editor.org/info/rfc8501).

- It is not unknown for some sites to register IPv4-mapped IPv6
  addresses, e.g. `::ffff:198.51.100.99`, with AAAA records. While this
  seems to work in most cases, it is inappropriate if the host in
  question has a valid IPv6 address, and pointless otherwise.

- Certain IPv6 address types should __never__ be visible in global DNS:
  ULAs (starting with `fdxx:` or even `fcxx:`) or link-local (starting
  with `fe80::`). Beware that automated mechanisms like Active Directory
  might add ULAs to global DNS by default. Of course, it is OK to
  include ULAs in _local_ DNS if a split DNS configuration is used.

  _Note:_ Some AAAA records for ULA addresses do exist in the DNS, and
  are not a security risk, but they may cause unexpected failures from a
  user's standpoint.

Some statistics on AAAA records and reachability may be found at
[Dan Wing's site](https://www.employees.org/~dwing/aaaa-stats/).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Managed%20configuration.md) [<ins>Next</ins>](Routing.md) [<ins>Top</ins>](2.%20IPv6%20Basic%20Technology.md)

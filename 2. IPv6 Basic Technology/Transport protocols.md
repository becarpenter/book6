## Transport protocols

Applications can readily be updated to work in dual stack mode, because
the transport layer is affected very little by IPv6. Therefore, IPv6
supports all the common transport protocols:

- UDP. There is no separate specification for UDP over IPv6;
  [RFC 768](https://www.rfc-editor.org/info/rfc768) still applies!
  However, the UDP checksum is mandatory for IPv6 (since the IPv6 header
  itself has no checksum), except as allowed by
  [RFC 6936](https://www.rfc-editor.org/info/rfc6936).

- UDP-lite \[[RFC3828](https://www.rfc-editor.org/info/rfc3828)\] also
  supports IPv6. There is interesting background on UDP and UDP-lite in
  [RFC 8304](https://www.rfc-editor.org/info/rfc8304).

- TCP. IPv6 support is fully integrated in the latest TCP standard
  \[[STD7](https://www.rfc-editor.org/info/std7)\].

- RTP fully supports IPv6
  \[[RFC3550](https://www.rfc-editor.org/info/rfc3550)\].

- QUIC fully supports IPv6
  \[[RFC9000](https://www.rfc-editor.org/info/rfc9000)\].

- SCTP fully supports IPv6
  \[[RFC4960](https://www.rfc-editor.org/info/rfc4960)\].

- MPTCP fully supports IPv6
  \[[RFC8684](https://www.rfc-editor.org/info/rfc8684)\].

Also, the secure transports TLS, DTLS and SSL all work normally with
IPv6. So does SIP (Session Initiation Protocol
\[[RFC3261](https://www.rfc-editor.org/info/rfc3261)\]), which does not
require NAT traversal support (STUN) in the case of IPv6.

All quality of service and congestion control considerations should be
approximately the same for IPv4 and IPv6. This is why
[RFC 2474](https://www.rfc-editor.org/info/rfc2474) defined
differentiated services identically for both versions of IP, and the
same applies to ECN (Explicit Congestion Notification
\[[RFC3168](https://www.rfc-editor.org/info/rfc3168)\]).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Routing.md) [<ins>Next</ins>](Extension%20headers%20and%20options.md) [<ins>Top</ins>](2.%20IPv6%20Basic%20Technology.md)

## Benchmarking and monitoring

Tody, IPv6 monitoring is often forgotten, ignored or done from the wrong
vantage point.

Some examples from experience:

- Large corporate network with no IPv6 monitoring, because the part of
  the network where the monitoring system was located had no IPv6.

- Web services with AAAA records
  \[[2. DNS](../02.%20IPv6%20Basic%20Technology/DNS.md)\] and proper
  configuration; monitoring indicated that everything was okay, but
  users could not access the web services via IPv6 from the Internet.
  Someone forgot a firewall rule, and the monitoring system was on the
  inside of the network.

- Mail (SMTP) server with AAAA records. However, IPv6 was disabled (or
  blocked by a firewall) for whatever reason, but nobody removed the
  AAAA records. Wasn't noticed internally, i.e. they did not monitor via
  IPv6.

There is no fundamental difference between monitoring services for IPv4
or IPv6; it just has to be done for all services and, if they are
dual-stacked, for both protocols.

In case of the mail server example above, there were probably three
different teams involved and they either didn't talk to each other or
had an inadequate process implemented and no automation.

Related to this, implementing IPv6 also gives an operator the chance to
clean up operational documentation, ops infrastructure and NOC
processes. It may also be an oportunity to implement more automation.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Remote%20configuration.md) [<ins>Next</ins>](Routing%20operation.md) [<ins>Top</ins>](06.%20Management%20and%20Operations.md)

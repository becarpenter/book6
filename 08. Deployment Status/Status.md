## Status

When speaking of IPv6, a question immediately comes up: "How many people
do use IPv6 on the Internet?". Answering this question is fundamental to
get an immediate understanding of the real adoption of IPv6. A recent
overview is presented in
[RFC 9386](https://www.rfc-editor.org/info/rfc9386).

A count of IPv6 users is monitored by various organizations. For
example, both
[Facebook](https://www.facebook.com/ipv6/?tab=ipv6_total_adoption) and
[Google](https://www.google.com/intl/en/ipv6/statistics.html) provide
statistics on the users that access their services over IPv6. A very
informative blog was posted in 2023 by
[Cloudflare](https://blog.cloudflare.com/ipv6-from-dns-pov), showing
that humans use IPv6 a lot more than bots, which seem to prefer IPv4. At
the end of 2023, Google and Cloudflare roughly agreed on 46% adoption by
worldwide users.

[Akamai](https://www.akamai.com/internet-station/cyber-attacks/state-of-the-internet-report/ipv6-adoption-visualization)
provides data measuring the number of hits to their content delivery
platform. For example, they showed 72% adoption in India in early 2024.

[APNIC](https://stats.labs.apnic.net/ipv6) quantifies the use of IPv6 by
means of a script that runs on Internet browsers.

Some statistics on DNS records and reachability for top web sites may be
found at
[Dan Wing's site](https://www.employees.org/~dwing/aaaa-stats/). These
data suggest 29% IPv6 penetration by July 2023.

At the time of writing, there are large discrepancies between data from
these and other sources. In fact there is no well-defined metric for
"how many IPv6 users exist" or "how much IPv6 traffic exists". To take
one example, Google estimates the fraction of Google "hits" that use
IPv6, yet Google is very little used in China so these data cannot
represent the true world-wide situation. Estimates posted to the IETF by
Geoff Huston in July 2023 suggest that Google observes a 7% adoption
rate in China, while the APNIC measurement reports 30%.

We show here the APNIC presentation of results, as it comes from a
Regional Internet Registry (RIR) to show the number of the Internet IPv6
users compared with the total Internet population (in million, see next
table).

<img src="./Section5_Table1.jpg" alt="Table shows 25% annual IPv6 growth 2018 to 2022">

A third of the Internet population apparently employs IPv6. It is also
interesting to look at the growth curve. The main indicator here is the
Compound Annual Growth Rate (CAGR), which shows a two-digit growth
across the 5-year period 2018-2022.

There is a caveat, though, we may want to consider. The method used by
APNIC cannot be fully employed in China, due to local policy filtering
traffic from abroad. An independent
[Chinese research](https://www.china-ipv6.cn/#/activeconnect/simpleInfo)
reports 713 million measured IPv6 customers as of September 2022,
against the 220 million reported by APNIC. If we add the difference
between the two statistics to the global count, we end up with a Ratio
of 43.68% in September 2022, not that far from the "psychological"
threshold of 50%.

In August 2025, China’s Cyberspace Administration announced that by June,
China had 834 million active IPv6 users, i.e., __75.29%__ of Chinese Internet users.
66% of traffic on mobile networks ran over IPv6, vs 28.32% on fixed networks.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Deployment%20by%20carriers.md) [<ins>Top</ins>](08.%20Deployment%20Status.md)

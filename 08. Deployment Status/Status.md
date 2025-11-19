## Status

When speaking of IPv6, a question immediately comes up: "How many people
currently use IPv6 on the Internet?". Answering this question is fundamental to
gain an understanding of the real adoption of IPv6. A 2023
overview is presented in
[RFC 9386](https://www.rfc-editor.org/info/rfc9386).

A count of IPv6 users is monitored by various organizations. For
example, both
[Facebook](https://www.facebook.com/ipv6/?tab=ipv6_total_adoption) and
[Google](https://www.google.com/intl/en/ipv6/statistics.html) provide
statistics on the users that access their services over IPv6. The 
results are different, due to different methods being used.
Google generally sees more IPv6 usage than Facebook, but Google
has a blind spot in China where adoption is significant.

A trusted source from a Regional Internet Registry (RIR)
is [APNIC Labs](https://stats.labs.apnic.net/ipv6/).
This site measures _capability_ rather than traffic or active users,
so the data should not be directly compared with Google or Facebook.
APNIC quantifies the availability of IPv6 by means of a script that
runs on Internet browsers.

A very informative blog was posted in 2023 by
[Cloudflare](https://blog.cloudflare.com/ipv6-from-dns-pov), showing
that humans use IPv6 a lot more than bots, which seem to prefer IPv4.
Cloudflare's current protocol usage data is summarized by
[Cloudflare radar](https://radar.cloudflare.com/).

[Akamai](https://web.archive.org/web/20250324111641/https://www.akamai.com/internet-station/cyber-attacks/state-of-the-internet-report/ipv6-adoption-visualization)
formerly provided data measuring the number of hits to their content delivery
platform. For example, they showed 72% adoption in India in early 2024.

In late 2025, Google, Facebook and Cloudflare roughly agreed on
40 to 50% worldwide adoption by users, with APNIC Labs showing 42%
IPv6 capability.

Some statistics on DNS records and reachability for top web sites may be
found at
[Dan Wing's site](https://www.employees.org/~dwing/aaaa-stats/). These
data suggest that only 30% of sites had IPv6 DNS entries by November 2025.
So while major sites are seeing up to 50% IPv6 usage, most smaller sites
are not even in the game.

At the time of writing, there are significant discrepancies between data from
these and other sources. In fact there is no well-defined metric for
"how many IPv6 users exist" or "how much IPv6 traffic exists". To take
one example, Google estimates the fraction of Google "hits" that use
IPv6, yet Google is very little used in China so these data cannot
represent the true world-wide situation. Estimates posted to the IETF by
Geoff Huston in July 2023 suggested that Google then observed a 7% adoption
rate in China, while the APNIC measurement reported 30% capability.


We show here an older APNIC presentation of results
to show the number of the Internet IPv6
users some years ago, compared with the total Internet population
(in millions, see next table).

<img src="./Section5_Table1.jpg" alt="Table shows 25% annual IPv6 growth 2018 to 2022">

A third of the Internet population apparently employed IPv6 then. It is also
interesting to look at the growth curve. The main indicator here is the
Compound Annual Growth Rate (CAGR), which shows a two-digit growth
across the 5-year period 2018-2022.

There is a caveat, however. The method used by
APNIC cannot be fully employed in China, due to local policy filtering
traffic from abroad. An independent
[Chinese research](https://www.china-ipv6.cn/#/activeconnect/simpleInfo)
reported 713 million measured IPv6 customers as of September 2022,
against the 220 million reported by APNIC. If we added the difference
between the two statistics to the global count, we would end up with a usage
of 43% in September 2022. (As it happened, the Google worldwide measurement
in that month peaked at 41%.) 

In August 2025, China’s Cyberspace Administration announced that by June,
China had 834 million active IPv6 users, i.e., 75% of Chinese Internet users.
66% of traffic on mobile networks ran over IPv6, vs 28% on fixed networks.
By October 2025,
[Chinese media claimed 77% adoption](https://www.chinadaily.com.cn/a/202510/31/WS690473f6a310f735438b8167.html).

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Deployment%20by%20carriers.md) [<ins>Top</ins>](08.%20Deployment%20Status.md)

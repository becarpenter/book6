## Source and Destination address selection

As described in
\[[2. Addresses](../02.%20IPv6%20Basic%20Technology/Addresses.md)\], a
host will have more than one IPv6 address per interface. Because of the
presence of multiple addresses in the same address family, there must be
a process for selecting the source and destination address pair for
general use. This address selection is described in
[RFC 6724](https://www.rfc-editor.org/info/rfc6724) and further, more
complex topics and scenarios can be found in the
\[[6. Multi-prefix operation](../06.%20Management%20and%20Operations/Multi-prefix%20operation.md)\]
section. Address selection is complicated by the flexibility that is
afforded by the multi-addressing nature of IPv6, and the ability for a
given host and applications ability to further define behavior. Server
applications are the best example of an application prescriptively
defining a specific address with which to source traffic. In the case
that an application specifies a specific address, then the process
generally stops there for that particular traffic, the host is not
required to further evaluate and the traffic in question is sourced from
the address specified by the given application.

In cases where there is no specificity by a given application, the
operating system will evaluate the available addresses of both IPv4 and
IPv6 address families and sort them according to a set of rules,
returning the top address from its evaluated list based on the pair of
source address and destination addresses, often shortened to "SA/DA" for
documentation and brevity. The sorting is done in order, and ceases once
a match is made. Address pairs for given traffic is evaluated in the
following order:

1. Prefer same address contacted
1. Prefer appropriate address scope
1. Avoid deprecated addresses
1. Prefer home addresses
1. Prefer outgoing interface
1. Prefer matching address label
1. Prefer privacy addresses
1. Use longest matching prefix

The default sorting behavior is generally defined by the following
table:

```
Prefix                            Prec   Label      
::1/128                           50     0    
::/0                              40     1  
::ffff:0.0.0.0/96                 35     4   
2002::/16                         30     2        
2001::/32                          5     5        
fc00::/7                           3    13   
::/96                              1     3       
fec0::/16                          1    11        
3ffe::/16                          1    12        
```

### Destination address selection

Destination address selection is somewhat complex, and it should be
understood that it is configurable and may be somewhat inconsistent
based on the implementation of a given IPv6 network stack and the age of
the operating system. At the time of this writing there are still
operating systems that employ aspects of or full implementations of
[RFC 3484](https://www.rfc-editor.org/info/rfc3484), which was obsoleted
by [RFC 6724](https://www.rfc-editor.org/info/rfc6724) in 2012. To fully
understand address selection, one can reference the file _/etc/gai.conf_
in a modern Linux system as it has the most succinct example of the
rules governing the process.

### Changing address selection policy

In the vast majority of use cases, the default policy table is unchanged
and consistent. However, on platforms such as Linux and Microsoft
Windows, it is possible to adjust this table to create desired behavior,
up to and including creating address pairings, adjusted preferences, and
unique traffic SA/DA characteristics.

A site using DHCPv6 options 84 and 85 can change the default settings
for address selection via
[RFC 7078](https://www.rfc-editor.org/info/rfc7078), but unfortunately
this is not widely implemented. In principle this can also be achieved
by system commands in each host (e.g. _netsh interface ipv6 add
prefixpolicy_ in Windows and _ip addrlabel add prefix_ in Linux) but
this is rarely done. The result is that hosts generally apply the
default policy for their operating system release, even when a different
policy would work better.

### ULA considerations

In default situations where both IPv4 and ULA are present, IPv4 will be
the preferred protocol. This is often counter to general understanding
of how IPv6 behavior works in a dual stacked environment and can be
observed in the aforementioned _gai.conf_ file with the following line:

```
Prefix                            Prec   Label      
...
::ffff:0.0.0.0/96                 35     4
```

This is the IPv6 conversion of IPv4 address space. Because this block of
addresses has a higher preference value than ULA addressing, it will be
preferred by default by the operating system and application due to its
preference value.

[draft-ietf-v6ops-ula](https://datatracker.ietf.org/doc/draft-ietf-v6ops-ula/)
described in detail many of the considerations for use of ULA,
specifically in a dual stacked environment. It should be noted that in
an IPv6-only environment, the address selection process is generally
problem free, leveraging the above process.

### Labels

Not to be confused with flow labels, address labels are a powerful and
often overlooked tool in the selection process. Address labels allow for
prefix or address pairings thus forcing traffic pairs to act in
consistent or desirable ways that may differ from default for technical,
security, or policy reasons. Taking a basic Linux system and creating an
address pair with matching labels will cause the system to act on the
labels and generate traffic between the SA/DA pairs as determined by the
operator.

Using a vanilla linux system the following changes can be made using the
ip command `{ip addrlabel add prefix <PREFIX> label <LABEL>}` easily
creating a working SA/DA pair.

For example:

```
sudo ip addrlabel add prefix fd68:1e02:dc1a:9:ba27:ebff:fe84:781c/128 label 97
sudo ip addrlabel add prefix 2001:db8:4009:81c::200e/128 label 97
```

Yields:

```
user@v6host:~$ sudo ip addrlabel list
prefix 2001:db8:4009:81c::200e/128 label 97
prefix fd68:1e02:dc1a:9:ba27:ebff:fe84:781c/128 label 97
prefix ::1/128 label 0
prefix ::/96 label 3
prefix ::ffff:0.0.0.0/96 label 4
prefix 2001::/32 label 6
prefix 2001:10::/28 label 7
prefix 3ffe::/16 label 12
prefix 2002::/16 label 2
prefix fec0::/10 label 11
prefix fc00::/7 label 5
prefix ::/0 label 1
```

### Source address selection

In practice, source address selection is difficult to configure outside
of link local, GUA, and ULA default preferences, and varies by host and
application implementations. It is possible to create address pairings
using the IPv6 address label mechanisms, however.

<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Traffic%20class%20and%20flow%20label.md) [<ins>Next</ins>](../03.%20Coexistence%20with%20Legacy%20IPv4/03.%20Coexistence%20with%20Legacy%20IPv4.md) [<ins>Top</ins>](02.%20IPv6%20Basic%20Technology.md)

## Basic Linux Commands

In this chapter we'll take a look at some of the most common
Linux commands to operate and troubleshoot IPv6.

Most tools use -4 or -6 as a parameter to select the protocol
version. There are some tools that are deprecated, but you still
find them in a lot of documentation, even current one. The most
common of these are *ifconfig* and *route* which are replaced
by *ip* and *netstat* which is replaced by *ss* (socket stat).

All tools mentioned here should have a comprehensive manual page,
and it is highly recommended that you read those.

Some configuration items are specific to the Linux-Distribution
you are using, so please check the documentation for your Linux
distribution as well.

### ip

The name *ip* might suggest that it is only used for *ip* related
configurations, but that is not the case. Let's start with
layer two related configuration and then go up. Note that *ip* has many
more features, and we will only cover the basics here.

Note that you can abbreviate the options, e.g. instead of *ip* address
show you can use *ip a s* or even *ip a*. There are also some usefull
options to modify the output of *ip*:

* -br - which gives you briefer output which is easier to parse in your own scripts
* -color - as the name implies you get a colored output
* -json - The output of the *ip* command will be JSON (JavaScript Object Notation)

Just calling ip without any parameters will give you the following output.

```
Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }
       ip [ -force ] -batch filename
where  OBJECT := { address | addrlabel | amt | fou | help | ila | ioam | l2tp |
                   link | macsec | maddress | monitor | mptcp | mroute | mrule |
                   neighbor | neighbour | netconf | netns | nexthop | ntable |
                   ntbl | route | rule | sr | tap | tcpmetrics |
                   token | tunnel | tuntap | vrf | xfrm }
       OPTIONS := { -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] |
                    -h[uman-readable] | -iec | -j[son] | -p[retty] |
                    -f[amily] { inet | inet6 | mpls | bridge | link } |
                    -4 | -6 | -M | -B | -0 |
                    -l[oops] { maximum-addr-flush-attempts } | -br[ief] |
                    -o[neline] | -t[imestamp] | -ts[hort] | -b[atch] [filename] |
                    -rc[vbuf] [size] | -n[etns] name | -N[umeric] | -a[ll] |
                    -c[olor]}
````

On a first, and maybe even the second or third glance this looks confusing, but
using *ip* is actually quite easy. There are options to modify the output, objects,
like link, neighbour, address and route which are followed by commands. The most
common commands are probably *show*, *add* and *delete*.  The show command should work as
normal user, other commands, like add or delete require higher privileges.

#### ip link

Let's start with our interfaces or link.

```
$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:07:bd:d7 brd ff:ff:ff:ff:ff:ff
```
We see that we have to interfaces, lo or loopback interface and enp1s0 which is an Ethernet interface. We see that both interfaces are UP some other inforation, inlcuding the MAC address of the interface. If we only want to see a specific interface, we can add that to the command line.

```
$ ip link show enp1s0
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:07:bd:d7 brd ff:ff:ff:ff:ff:ff
```

#### ip neigh

With the neighbour (here shortened to neigh) we can see our neighbour table.

```
$ ip -6 neigh show
fe80::2418:65ff:fe3e:8c4a dev enp1s0 lladdr 26:18:65:3e:8c:4a router REACHABLE
```

#### ip address


#### ip route


### ss


## Advanced Troubleshooting

- **Multicast Listener Discovery (MLD):** Ensure multicast listeners are
  operational, as NDP relies heavily on multicast.

- **Firewall and ACL Verification:** Ensure that firewalls or access
  control lists (ACLs) permit necessary IPv6 traffic.

Firewall policy should match between protocols wherever possible. ICMPv6
is a notable exception, due to the significant differences and notable
reliance on ICMPv6 for normal IPv6 function.

### Troubleshooting Dual-Stack Networks

In dual-stack environments, it is crucial to address complexities
stemming from simultaneous IPv4 and IPv6 operation:

- **Protocol Preference Issues:** Identify cases where applications or
  hosts may incorrectly prefer IPv4 over IPv6, or vice versa.

  ```bash
  # Check routing preference
  getent ahosts example.com
  ```

- **Service Availability:** Validate that network services (DNS, DHCP,
  web services) respond correctly for both IPv4 and IPv6 requests.

  ```bash
  dig A example.com
  dig AAAA example.com
  ```

- **Performance Baselines:** Continuously monitor dual-stack performance
  to detect and remediate suboptimal IPv6 connectivity.

### Happy Eyeballs Algorithm

The "Happy Eyeballs" algorithm (RFC 8305) optimizes dual-stack
experiences by dynamically choosing the protocol that provides the best
user experience:

- **Behavior Analysis:** Observe connections initiated by the
  application and verify if it appropriately falls back to IPv4 when
  IPv6 connectivity is poor or fails.
- **Timeout Adjustments:** Tune timers within applications to optimize
  the balance between IPv4 fallback speed and IPv6 preference.
- **Diagnostic Tools:** Utilize browser developer tools or packet
  captures (Wireshark, tcpdump) to monitor application behavior in
  real-time.

### Troubleshooting Translation Mechanisms

**DNS64**\
Verify DNS64 functionality by ensuring AAAA record synthesis
for IPv4-only services. Monitor responses with:

```bash
dig AAAA ipv4-only-domain.example
```

**NAT64**\
Confirm NAT64 translations with state tables and packet
captures to verify proper address and port mappings.

```bash
# Inspect NAT64 mappings
show nat64 translations
```

**pref64**\
Check prefix discovery mechanisms used by hosts to determine
NAT64 prefix.

```bash
ip -6 route show
```

### IPv6-only Networks

Validate services and applications compatibility in IPv6-only
environments. Test DNS, DHCPv6, and ensure no IPv4 dependencies remain:

```bash
ping6 ipv6-only-host.example
```

### Multicast Issues

**Wireless and Wireless Controllers**\
Ensure multicast traffic is
permitted and configured correctly on wireless controllers to support
IPv6 multicast applications.

**Router Advertisement Issues**\
Check proper Router Advertisement (RA)
dissemination, ensuring routers advertise correct prefixes and default
routes:

```bash
tcpdump -i eth0 icmp6 and ip6[40] == 134
```

### Host-Based Firewalls

Inspect host firewall rules to verify they permit essential IPv6 traffic
(ICMPv6, DHCPv6, and required application ports):

```bash
iptables -L -n -v -6
```

### ICMPv6 and Filtering

ICMPv6 is critical for IPv6 functionality, including path MTU discovery,
neighbor discovery, and diagnostics. Ensure ICMPv6 messages are
permitted and properly handled:

```bash
tcpdump icmp6
```

<!-- Link lines generated automatically; do not delete -->

### [<ins>Next</ins>](Tools.md) [<ins>Top</ins>](09.%20Troubleshooting.md)

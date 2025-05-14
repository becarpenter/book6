## Basic Windows commands

To determine current IPv6 configuration, type `ipconfig /all` at the Windows command prompt.

Both `ping` and `tracert` work normally for IPv6. In the case of link-local addresses,
Windows supports the default zone identifier (also known as the default interface),
so `ping fe80::1234` will automatically use the default interface. On a host with more
than one network interface, the interface may be specified, e.g. `ping fe80::1234%7`.
The interfaces in use can be found in the output from `ipconfig /all`.

To check or change basic IPv6 configuration, use
`Control Panel/All Control Panel Items/Network and Sharing Center/Change Adapter Settings`.
Select the network adapter of interest, then `Properties/Internet Protocol Version 6`
and basic properties will be available. Normally, nothing will need to be changed.

More advanced properties can be checked or changed from the command prompt with `netsh`, e.g.,
`netsh interface ipv6 show privacy` to show whether temporary addresses are active.
Since `netsh` is a very complex tool, we do not fully describe it here, but it includes
on-line help at every level, by adding `?` to a command, e.g., `netsh interface ipv6 show interfaces ?`.

The same functionality (and more) is also available using PowerShell,
for which we suggest seeking Microsoft documentation.


<!-- Link lines generated automatically; do not delete -->

### [<ins>Previous</ins>](Packet%20size%20and%20Jumbo%20Frames.md) [<ins>Next</ins>](../07.%20Case%20Studies/07.%20Case%20Studies.md) [<ins>Top</ins>](06.%20Management%20and%20Operations.md)

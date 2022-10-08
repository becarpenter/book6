## How an application programmer sees IPv6

In a very theoretical world, an application programmer could rely on
a DNS lookup to return the best (and only) address of a remote host,
and could then pass that address directly to the network socket
interface without further ado. Unfortunately the real world is not
that simple. Even without considering the version number, there are
several types of IP address, and a DNS lookup may return a variety
of addresses. In most cases, applications will use the function
```getaddrinfo()``` ("get address information") to obtain
a list of valid addresses. Which is
the best one to use, and should the program try more than one?

We do not go into this subject in detail, because this book is
not aimed primarily at application programmers. However, operators
need to be aware that the default behavior of most applications
is simply to use the *first* address returned by ```getaddrinfo()```.
Some applications (such as web browsers) may use a smarter approach
known as "happy eyeballs" ([RFC8305](https://www.rfc-editor.org/info/rfc8305)) by means of a heuristic to detect which
address gives the fastest response. However, operators need to
understand the various address types in order to configure
systems optimally, including the ```getaddrinfo()``` precedence
table ([RFC6724](https://www.rfc-editor.org/info/rfc6724)) in every host.

Address types are discussed further in [2. Addresses](../2.%20IPv6%20Basic%20Technology/Addresses.md).

<!-- Link lines generated automatically; do not delete -->
### [<ins>Previous</ins>](How%20a%20user%20sees%20IPv6.md) [<ins>Next</ins>](How%20a%20network%20operations%20center%20sees%20IPv6.md) [<ins>Chapter Contents</ins>](1.%20Introduction%20and%20Foreword.md)

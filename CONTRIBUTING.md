# book6 - a collaborative IPv6 book.

This file describes how to contribute.

Contributors will be self-declared practitioners of IPv6. There is no other entry ticket except a valid GitHub account.

Contributions (in GitHub markdown format) will fit into an agreed [table of contents](Contents.md). They will be factual and will teach technical readers about a particular aspect of IPv6. As far as possible, references will be to RFCs and other freely available documents.

Where there are alternatives and choices for people deploying or using IPv6, the choices will be presented objectively, if possible with factual pros and cons. Justified recommendations may be made (e.g., "X is generally more secure than Y") but strong personal opinions (e.g., "NAT66 is never the right answer") should be avoided.

Contributors may edit their own and other contributions. However, significant changes should first be discussed using the issue tracker. That isn't necessary for spelling mistakes, grammar problems, or small nits. GitHub PRs will be used when necessary (i.e., where the additions or changes need review). The goal is to achieve IETF-style rough consensus on the content. A typical tie-breaker argument is "I have deployed this and it works well."

Normal, a contribution will be a complete section. There is a naming convention for files, based on the table of contents, so that we can write a script to generate the whole book from the repo. See the [basic chapter template](99.%20Chapter%20Template/99.%20Chapter%20Template.md) and follow it carefully.
That chapter also contains instructions for the use of GitHub markdown.  Please create a separate file for each section within the folder for its chapter. See the chapter template itself for detailed instructions. If you don't follow these instructions, things will get messed up and will need to be sorted out manually.

If you prefer to submit a PR containing plain text, somebody will eventually add markdown, but there may be a delay. Please don't submit other formats.

Note that contributions **MUST** be original writing unless the contributor has the legal right to submit existing material under the agreed license (see [LICENSE.md](LICENSE.md)).

If we use direct quotations from RFCs they **MUST** be small extracts that can be considered "fair use" as mentioned in the relevant [IETF Trust FAQ](https://trustee.ietf.org/about/faq/#reproducing-rfcs) under "Am I allowed to reproduce extracts from RFCs?" However, *modified* extracts from RFCs are not allowed.

(For avoidance of doubt, if *you* personally are the copyright holder of original material, *you* may contribute it here and modify it under [LICENSE.md](LICENSE.md) even if it has also been contributed to an RFC.)

We will appoint two or three people as top-level editors who can declare consensus and approve PRs.

The language is English, preferably US spelling. Please keep sentences reasonably short and simple. Avoid language that might be unclear for someone whose first language is not English. Avoid terminology that is inappropriate in professional writing. In case of doubt, please consider the archived [NIST guidance on inclusive language](https://web.archive.org/web/20250203031433/https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8366.pdf). If adding diagrams, please consider accessibility by the visually impaired and ensure that alternative text is provided.

Any translation into other languages must be under the same open source license as the original version and must be available free of charge.

# README for book6/utilities

This directory contains a few items that are not part of the book itself but are useful anyway.

In particular there's [makeBook](./makeBook.py), whose job is to reconcile book6 chapters with
contents, and set up inter-section and inter-chapter links as far as possible. Please don't run
it unless you know what you're doing. Similarly, [indexBook](./indexBook.py) updates the index
(based on index terms in [index6.txt](./index6.txt)) and [RFCbib6.py](./RFCbib6.py) rebuilds
the RFC citation index.

[bakeBook](./bakeBook.py) "bakes" all the sections of book6 into a single markdown file, used
to generate a PDF version of the book.

These utilities are documented in [utDoc.md](./utDoc.md).

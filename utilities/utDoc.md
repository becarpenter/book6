## The book6 utilities

### makeBook

This program is applied to the entire book6 directory
whenever significant changes have been made. The reader 
is assumed to have carefully read the 
[Chapter Template](https://github.com/becarpenter/book6/blob/main/99.%20Chapter%20Template/99.%20Chapter%20Template.md)
chapter.

__makeBook__'s functions include:

 - Update the global contents (_Contents.md_) to reflect the actual chapter contents.

 - Update the individual chapter files (_./ChapterName/ChapterName.md_) to correspond to the global contents.

 - Create any missing section files (_./ChapterName/SectionName.md_).

 - Reconcile discrepancies between the global contents, the chapter
contents, and the actual section files. (Not all discrepancies can
be automatically reconciled - __makeBook__ will issue a warning if it
detects such a case).

 - Resolve any raw citations (`{{something}}` or `{{{something}}}`)
into a complete markdown link (`[something](URL)`).

 - Create and insert internal links (from a chapter file to the
individual sections, from each section to its predecessor and
successor, etc.)

 - Reformat markdown text if appropriate.

After updating a section, especially if adding a new citation
with `{{ }}` or `{{{ }}}`, it's appropriate to run __makeBook.py__ 
(Python 3; requires _tkinter_; uses _mdformat_ if installed).

To make changes other than just updating an existing section, 
also see [chapterReorg](./chapterReorg.md).

__makeBook__ works roughly as follows, using a _tkinter_ GUI, not
standard input.

1. Request name of _book6_ directory from user. Normally this
will be the local copy of the GitHub repo.

2. Determine whether automatic checking of RFC existence is
possible. If __makeBook__ cannot access a recent copy of the RFC
index, this checking is impossible and it logs a warning.

3. Determine whether automatic checking of I-D existence is
possible. If __makeBook__ cannot access the current I-D index,
this checking is impossible and it logs a warning.

4. Read in the existing main contents (_Contents.md_).

5. Convert any plain text chapter names to links.

6. Scan main contents and create any missing chapter directories
and blank chapter files, build a chapter list, extract
section lists for each chapter, and add any missing section
names to the main contents.

7. For each chapter:

  * 7.1 If there is a remaining discrepancy between
the list of sections in the main contents and the section
files actually present, log a warning that __makeBook__ must
be run again to resolve it. Also log a warning if there is
an uppercase/lowercase discrepancy (which really needs
manual fixing).

  * 7.2 Create and initialize any missing section files.

  * 7.3 If anything in the chapter file has changed during
steps 7.1 and 7.2 , write it back.

  * 7.4 For each section in the chapter:  

    * 7.4.1 Read in the markdown file, update internal links
if necessary, expand any `{{ }}` or `{{{ }}}` citations
as markdown links (but log a warning if this fails).

    * 7.4.2. If anything in the section file has changed during
step 7.4.1, write it back.

  * 7.5. Read in the chapter markdown file (again),
expand any `{{ }}` or `{{{ }}}` citations as markdown links
(but log a warning if this fails), and write it back
if necessary.

8. Finally, write back the main contents.

Note that expanding citations is done by the function
_expand_cites()_ which is straightforward but tedious
to describe.

__makeBook__ issues warnings to standard output but also
to the file _makeBook.log_ in the main book6 directory.
This log should always be checked after a run!


### indexBook

This program is applied to the entire book6 directory. It reads
each section file in each chapter, and if one of the index terms
in file _./utilities/index6.txt_ is present, an index entry is
created or extended, pointing to the section. 

Index terms are not case-sensitive, and each term can appear
in several variants. The details of that are given in
_index.txt_ itself, but for example the line
~~~
link-local 'link local' link-locals
~~~
means that all three terms will be indexed under `link-local`.

The program also builds a citation index, showing which RFCs
are indexed by which sections.

At the end, the collated and sorted results are written to _./Index.md_
and _./Citex.md`_

__indexBook__ issues warnings to standard output but also
to the file _indexBook.log_ in the main book6 directory.
This log should always be checked after a run!

### RFCbib6

This program creates a list of all current RFCs that
mention IPv6 in their title or come from the major IPv6 working groups.
Obsolete RFCs are not included. There are subsections for Standards, BCPs, 
Informational and Experimental RFCs. It does this by processing a recent
copy of the RFC index (in XML format) according to the above criteria.
The result is stored as a book6 chapter in
_./20. Further Reading/RFC bibliography.md_.

__RFCbib6__ issues warnings to standard output but also
to the file _RFCbib6.log_ in the main book6 directory.
This log should always be checked after a run!

It's best to run __makeBook__ afterwards. (Note that _RFC bibliography.md_
is ignored by __indexBook__, to avoid noise in the citation index.)

### bakeBook

This program concatenates the whole book into a single "baked"
markdown file (called _baked.md_). This isn't intended for users,
but as an intermediate step on the way to a PDF version of
book6.

Its main job, apart from concatenating all relevant .md files,
is to fix up internal references to match the way GitHub
creates anchors for chapter and section titles in `## Title`
format. The code is very ad hoc and has to special-case
a few details.

The title page is at _Title.md_ and is augmented during
baking by adding a timestamp.

One gotcha is that all graphics files (`.png, .jpg`, etc.)
needed to be copied into the main directory, and their names
must be unique book-wide. Another gotcha
is that section names must also be unique book-wide.

A necessary hack is that where a page break is needed,
this is signaled by a dummy line: `backslashpagebreak`.
This is converted later to a genuine pagebreak.

Further info is in the `pdf` directory.


This folder `pdf` is used for generating a complete PDF file of book6 and is not otherwise interesting.

As of 2024-04-11 the contents of this folder are work-in-progress and not aimed at readers.

The image files are duplicated here intentionally.

The intermediate file `baked.md` is a complete markdown of the whole book, made by the `bakeBook.py` utility. The utility also attempts to convert `baked.md` first to LaTeX as `baked.tex` and then to PDF as `baked.pdf`. If this fails, try the following manual process.

First convert to LaTeX using pandoc:

```
pandoc baked.md -f gfm -t latex -s -o baked.tex -V colorlinks=true
```

Then comes the tricky bit. _Manually edit_ `baked.tex` with any text editor, changing all occurrences of `backslashpagebreak` to `\pagebreak`.

Then convert the LaTeX file to PDF. Good results on Windows are obtained using `TeXworks` or the command `pdflatex baked.tex` (the latter needs to be run twice to satisfy references).
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bake book6 into a single markdown file, then PDF and EPUB"""

# Version: 2024-01-14 - original
# Version: 2024-01-17 - case error in index citations
#                     - fixed missing special cases for citations
#                     - replace blobs with pilcrows for latex
# Version: 2024-01-18 - skip code blocks when fixing citations
# Version: 2024-01-29 - use dedicated pdf directory
# Version: 2024-04-02 - copy image files to pdf directory
# Version: 2024-04-04 - change image citations to suit pandoc
# Version: 2024-04-07 - deprecate SVG to suit pandoc
#                     - added pagebreak hack
# Version: 2024-04-08 - cosmetic fix
# Version: 2024-04-11 - attempt PDF conversion
# Version: 2024-04-28 - handle directory on command line
# Version: 2024-08-19 - adjust alt text handling for graphics
#                     - added EPUB conversion
# Version: 2024-08-20 - fixed case error in "Title.md"
# Version: 2024-09-24 - adapt to Contents.md with embedded links
# Version: 2025-02-01 - Make epub more readable, linting
# Version: 2025-02-05 - Avoid pagebreak on epub title page

########################################################
# Copyright (C) 2024 Brian E. Carpenter.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with
# or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above
# copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of
# its contributors may be used to endorse or promote products
# derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
# AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
########################################################

from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel, askyesno, showinfo

import time
import os
import sys
import subprocess
import shutil


def show(msg):
    """Show a message"""
    global T, cmd_line
    if cmd_line:
        print(msg)
    else:
        showinfo(title=T, message=msg)


def logit(msg):
    """Add a message to the log file"""
    global flog, printing
    flog.write(msg + "\n")
    if printing:
        print(msg)


def logitw(msg):
    """Add a warning message to the log file"""
    global warnings
    logit("WARNING: " + msg)
    warnings += 1


def dprint(*msg):
    """Diagnostic print"""
    global printing
    if printing:
        print(*msg)


def crash(msg):
    """Log and crash"""
    global printing
    printing = True
    logit("CRASH " + msg)
    flog.close()
    exit()


def rf(f):
    """Return a file as a list of lower case strings"""
    file = open(f, "r", encoding="utf-8", errors="replace")
    l = file.readlines()
    file.close()
    return l


def wf(f, l):
    """Write list of strings to file"""
    global written
    file = open(f, "w", encoding="utf-8")
    for line in l:
        file.write(line)
    file.close()
    logit("'" + f + "' written")


def cmd(command):
    """Execute system command"""
    do_cmd = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _out, _err = do_cmd.communicate()
    if _err:
        logitw(_err.decode("utf-8").strip())


##    if _out:
##        _out = _out.decode('utf-8').strip()
##        print(_out)


def uncase(l):
    """Return lower case version of a list of strings"""
    u = []
    for s in l:
        u.append(s.lower())
    return u


def fix_section(raw, epub=False):
    """Change citations and images throughout a section"""
    new = []
    skipping = False
    first_line = True
    is_toc = False
    for line in raw:
        if epub and is_toc and line.startswith("##"):  # TOC
            new.append("\n\n")
            return new
        if epub and first_line:
            first_line = False
            if line.startswith("# "):  # it's a chapter TOC
                is_toc = True
        # latex doesn't like the blob character
        if "●" in line:
            line = line.replace("●", "¶")
        if line.startswith("```") or line.startswith("~~~"):
            if skipping:
                # already in a code block, back to normal processing
                skipping = False
            else:
                # entering a code block
                skipping = True
        if skipping:
            # skip processing to avoid damaging example citations
            new.append(line)
            continue
        if epub and (
            line.startswith("### [<ins>Next</ins>]")
            or line.startswith("### [<ins>Previous</ins>]")
        ):
            continue
        if "](" in line:
            # need to reformat citation
            outline = ""
            while "](" in line:
                head, line = line.split("](", maxsplit=1)
                if line.startswith("https:") or line.startswith("http:"):
                    outline += head + "]("
                    continue  # Web reference, nothing to change
                target, line = line.split(")", maxsplit=1)
                if "/" in target:
                    _, target = target.rsplit("/", maxsplit=1)
                if target[0].isdigit():
                    # Chapter number will not be in anchor
                    _, target = target.split("%20", maxsplit=1)
                if target.endswith(".md"):
                    target = target.replace(".md", "")
                target = target.replace("%20", "-").replace(".", "").lower()
                if target == "contents":
                    # Special case
                    target = "list-of-contents"
                if target == "index":
                    # Special case
                    target = "book6-main-index"
                if target == "citex":
                    # Special case
                    target = "book6-citation-index"
                outline += head + "](#" + target + ")"
            outline += line
        elif "<img src=" in line:
            # need to munge image reference for pandoc
            # (lazy, only handles the first one)
            head, tail = line.split("<img src=", maxsplit=1)
            # print(head, tail)
            try:
                img, tail = tail.split("/>", maxsplit=1)
            except:
                img, tail = tail.split(">", maxsplit=1)
            img = img.replace("'", '"')  # normalise string delimiters to "
            imgfile, imgalt = img[1:].split('"', maxsplit=1)
            imgfile = imgfile.replace("./", "")  # normalise image file name
            # extract alternative text
            try:
                _, imgalt = imgalt.split('alt="', maxsplit=1)
                imgalt, _ = imgalt.split('"', maxsplit=1)
            except:
                imgalt = "No description available"
            # build image citation as pandoc likes it.
            # the newlines avoid a layout mess
            ###outline = head+'\n\n![x]('+imgfile+' "'+imgalt+'")'+tail
            outline = head + "\n\n![" + imgalt + "](" + imgfile + ")" + tail
        else:
            outline = line
        # Avoid unwanted anchors
        if outline.startswith("## ["):
            # Assume this is a chapter contents item
            outline = outline[3:]
        # Cosmetic fix for links in PDF
        if "<ins>Chapter Contents</ins>" in outline:
            outline = outline.replace("<ins>Chapter Contents</ins>", "<ins>Top</ins>")
        new.append(outline)
    if epub:
        new.append("\n\n")
    else:
        new.append(page_break)
    return new


def imgcopy(dirname):
    """Duplicate any image files in the pdf directory"""
    for f in os.listdir(dirname):
        ftype = os.path.splitext(f)[1]
        if ftype == ".svg":
            logitw("SVG image found, probable pandoc failure")
        if ftype in [".svg", ".jpg", ".jpeg", ".png", ".gif"]:
            shutil.copy(dirname + "/" + f, "pdf/" + f)


page_break = "\nbackslashpagebreak\n"

######### Startup

# Define some globals

printing = False  # True for extra diagnostic prints
warnings = 0

cmd_line = False
if len(sys.argv) > 1:
    # user provided directory name?
    if os.path.isdir(sys.argv[1]):
        # assume user has provided directory
        # and set all options to defaults
        os.chdir(sys.argv[1])
        cmd_line = True

utility_dir = os.path.dirname(os.path.realpath(__file__))

# Announce
if not cmd_line:
    Tk().withdraw()  # we don't want a full GUI

    T = "Book baker."

    printing = askyesno(title=T, message="Diagnostic printing?")

    os.chdir(askdirectory(title="Select main book directory"))

# Open log file

flog = open("bakeBook.log", "w", encoding="utf-8")
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z", time.localtime())
logit("bakeBook run at " + timestamp)

logit("Running in directory " + os.getcwd())


show("Will read current book6 text.\nTouch no files until done!")


######### Create empty output

baked = []
epub_backed = []

######### Title page

title = rf("Title.md")
title.append("\nVersion captured at " + timestamp + "\n")
epub_backed += title
title.append(page_break)
baked += title
del title

######### Contents

# Read raw contents

contents = rf("Contents.md")

# Make list of section files to be baked, copy image files

preamble = True
fns = []
for line in contents:
    if line.startswith("[1. Introduction]"):
        preamble = False
    if preamble:
        continue  # ignore preamble
    if not line.strip():
        continue  # ignore blank
    if line.startswith("["):
        # directory name
        _, tail = line.split("](")
        dirname, filename = tail.split("/")
        dirname = dirname.replace("%20", " ")
        imgcopy(dirname)  # copy any image files
        filename = filename.replace("%20", " ").replace(")", "").replace("\n", "")
    elif line.startswith("* ["):
        # strip link
        filename, _ = line[3:].split("]", maxsplit=1)
        filename += ".md"
    elif line.startswith("*"):
        # old format (plain name)
        filename = line.replace("* ", "").replace("%20", " ").replace("\n", "") + ".md"
    fns.append(dirname + "/" + filename)

# Pre-bake contents

contents = fix_section(contents)

baked += contents

######### Main text

for fn in fns:
    baked += fix_section(rf(fn))
    epub_backed += fix_section(rf(fn), True)


######### Indexes

baked += fix_section(rf("Index.md"))
baked += fix_section(rf("Citex.md"))
epub_backed += fix_section(rf("Index.md"), True)
epub_backed += fix_section(rf("Citex.md"), True)

######### Write the baked file

wf("pdf/baked.md", baked)
wf("pdf/baked_epub.md", epub_backed)

######### Attempt LaTeX and PDF conversion
logit("Attempting LaTeX conversion")
try:

    # Call pandoc to make LaTeX file
    cmd(
        "pandoc pdf/baked.md -f gfm+implicit_figures -t latex -s -o pdf/baked.tex -V colorlinks=true"
    )

    # Fix up LaTeX
    latex = rf("pdf/baked.tex")
    for i in range(len(latex)):
        if "backslashpagebreak" in latex[i]:
            latex[i] = "\\pagebreak\n"
    wf("pdf/baked.tex", latex)

    # Convert LaTeX to PDF
    logit("Attempting PDF conversion (slow)")
    # Must switch to PDF directory
    os.chdir("pdf")
    cmd("pdflatex baked.tex")
    # 2nd run to fix citations
    cmd("pdflatex baked.tex")
    logit("Exiting PDF conversion - check baked.pdf")

except Exception as e:
    logitw("PDF conversion failure: " + str(e))
    logitw("Manual PDF conversion needed.")

######### Attempt EPUB conversion
logit("Attempting EPUB conversion (slow)")
try:
    metadata_file = os.path.join(utility_dir, "epubMetadata.yaml")
    css_file = os.path.join(utility_dir, "epub.css")
    font_file = os.path.join(utility_dir, "NotoSansMono-Regular.ttf")
    cmd(
        f"pandoc baked_epub.md -f gfm --toc=true -t epub3 -o baked.epub -V colorlinks=true --epub-title-page=false --metadata-file={metadata_file} --css {css_file} --epub-embed-font={font_file}"
    )
    logit("Exiting EPUB conversion - check baked.epub")

except Exception as e:
    logitw("EPUB conversion failure: " + str(e))
    logitw("Manual EPUB conversion needed.")

######### Close log and exit

flog.close()

if warnings:
    warn = str(warnings) + " warning(s)\n"
else:
    warn = ""

show(warn + "Check bakeBook.log.")

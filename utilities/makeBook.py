#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reconcile book6 chapters with contents, and set up inter-section
and inter-chapter links as far as possible."""

# Version: 2022-09-18 - original
# Version: 2022-09-26 - added {{{ }}} citations
# Version: 2022-10-05 - fencepost error when adding section to contents
# Version: 2022-10-06 - added citation expansion for chapter base file
# Version: 2022-11-09 - allow {{ }} as well as {{{ }}}
#                     - added citation of I-D. or draft-
# Version: 2022-11-15 - check that cited references exist (partial)
# Version: 2022-11-16 - improved reference checks (but still partial)
# Version: 2022-11-18 - small oversight in reference check
# Version: 2022-11-19 - cosmetic
# Version: 2022-11-20 - now checks I-D, BCP and STD refs
# Version: 2022-11-22 - fix oversights/nits in contents updating
# Version: 2022-11-27 - {{ }} now puts [ ] round citation
#                     - {{{ }}} does not put [ ]
#                     - fix missing newline when adding new section
# Version: 2023-01-10 - fix bug when adding new chapter name to Contents.md
#                     - enormous simplification of Contents creation
# Version: 2023-05-20 - skip on-line check for RFC bibliography
# Version: 2023-07-19 - apply mdformat to changed files
#                     - add global mdformat option
#                     - add mitigations for SSL certs for URL checking
# Version: 2023-08-03 - correctly ignore ``` blocks
# Version: 2023-08-10 - changed to use RFC index for existence checking
# Version: 2024-01-01 - changed default text for empty sections
# Version: 2024-04-12 - improved optics of RFC citations
# Version: 2024-04-28 - handle directory on command line
# Version: 2024-09-05 - insert section links in contents page
#                     - rename "Chapter Contents" link as "Top"
#                     - add next chapter links to last sections
# Version: 2024-09-13 - fix for internal cite of chapter name
# Version: 2024-11-16 - handle chapter with sections directly embedded
# Version: 2024-11-21 - allow RFC citations with #section
# Version: 2024-12-07 - tweaked handling of malformed citations
# Version: 2024-12-24 - switch to proper xml parser
# Version: 2025-01-06 - change sort order for chapter directories
#                     - and base files(prepend 0)
#                     - includes one-time fix-up for internal citations and
#                     - one-time renaming of old directories and base files
# Version: 2025-01-15 - give warning if cited I-D is replaced or missing
# Version: 2025-02-01 - linting
# Version: 2025-02-25 - allow for future format of RFC index (no leading zeros)


########################################################
# Copyright (C) 2022-2025 Brian E. Carpenter.
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
import sys
import os
import urllib.request
import ssl
import certifi
import requests
import xmltodict

try:
    import mdformat

    formatter = True
except:
    formatter = False


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
    printing = True
    logit("CRASH " + msg)
    flog.close()
    exit()


def rf(f):
    """Return a file as a list of strings"""
    file = open(f, "r", encoding="utf-8", errors="replace")
    l = file.readlines()
    file.close()
    # ensure last line has a newline
    if l[-1][-1] != "\n":
        l[-1] += "\n"
    return l


def wf(f, l, mdf=True):
    """Write list of strings to file"""
    global written
    file = open(f, "w", encoding="utf-8")
    for line in l:
        file.write(line)
    file.close()
    logit("'" + f + "' written")
    if mdf and formatter and f.endswith(".md"):
        mdformat.file(f, options={"wrap": 72})
        logit("'" + f + "' md formatted")
    written += 1


def uncase(l):
    """Return lower case version of a list of strings"""
    u = []
    for s in l:
        u.append(s.lower())
    return u


def make_basenames():
    """Make or refresh base names"""
    global base_names, base
    base_names = []
    for basex in range(len(base)):
        bline = base[basex]
        if len(bline) < 4:
            continue
        bline = bline.strip("\n")
        if bline.startswith("## ["):
            # existing section reference
            sname, _ = bline.split("[", maxsplit=1)[1].split("]", maxsplit=1)
            base_names.append(sname)
        elif bline.startswith("## ") and not "###" in bline:
            # possible new section
            # look ahead to see if there is embedded content
            linex = basex + 1
            content = False
            try:
                while not (
                    base[linex].startswith("## ")
                    or base[linex].startswith("### [<ins>Back")
                ):
                    if base[linex].strip() and not base[linex].startswith("<!--"):
                        # Some content is there
                        content = True
                        break
                    linex += 1
                if content:
                    # embedded section, do not add to base names
                    continue
            except:
                continue  # malformed file
            try:
                _, sname = bline.split(" ", maxsplit=1)
            except:
                continue  # malformed line
            # treat as new section (will create file later)
            base_names.append(sname)
    dprint("Base names: ", base_names)


def link_text(prev, nxt, chapter):
    """Construct link for end of a section"""
    part1 = ""
    part2 = ""
    if prev:
        part1 = " [<ins>Previous</ins>](" + prev.replace(" ", "%20") + ".md)"
    if nxt:
        part2 = " [<ins>Next</ins>](" + nxt.replace(" ", "%20") + ".md)"
    return (
        "###"
        + part1
        + part2
        + " [<ins>Top</ins>]("
        + chapter.replace(" ", "%20")
        + ".md)"
    )


link_warn = "<!-- Link lines generated automatically; do not delete -->\n"


def url_ok(url):
    """Check if a URL is OK"""
    global headers, context
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(
            request, context=context, timeout=30
        ).getcode()
    except Exception as E:
        # logitw(url+": "+str(E))
        return False  # URL doesn't work
    return response == 200


def draft_current(dr_name):
    """Check if an I-D is current"""
    global headers, context
    if dr_name.endswith("/"):
        dr_name = dr_name[:-1]
    if rfcs_checkable:
        if dr_name in all_ids:
            return False  # draft is now an RFC
    url = "https://datatracker.ietf.org/doc/" + dr_name
    # print(url)
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, context=context, timeout=30)
    except Exception as E:
        # print(str(E))
        return False  # URL for draft doesn't work
    if response.getcode() != 200:
        # print("Response code", response.getcode())
        return False  # URL for draft doesn't work
    html = response.read(30000).decode("utf-8")
    if "Replaced by" in html:
        return False  # draft is OBE
    # print("Not OBE")
    return True


def rfc_ok(s):
    """Check if an RFC etc. is real"""
    global rfcs_checkable
    if not rfcs_checkable:
        return True  # because we can't check on line right now
    sz = s[:3] + s[3:].zfill(4)  # zero-filled doc-id
    dprint("Checking", s)
    # This code will work before and after change in RFC-index format
    if s[:3] == "BCP":
        found = [r for r in all_bcps if r["doc-id"] in (s, sz)]
        # print(found)
        return len(found) == 1
    elif s[:3] == "STD":
        found = [r for r in all_stds if r["doc-id"] in (s, sz)]
        # print(found)
        return len(found) == 1
    elif s[:3] == "RFC":
        found = [r for r in all_rfcs if r["doc-id"] in (s, sz)]
        # print(found)
        return len(found) == 1
    else:
        return False  # invalid call


def draft_ok(s):
    """Check if a draft is real"""
    global drafts_checkable
    if not drafts_checkable:
        return True  # because we can't check on line right now
    dprint("Checking", s)
    # remove revision number if present
    if s[-3] == "-" and s[-2].isdigit() and s[-1].isdigit():
        s = s[:-3]
    url = "https://bib.ietf.org/public/rfc/bibxml3/reference.I-D." + s + ".xml"
    return url_ok(url)


def file_ok(fn):
    """Check if a local file is OK"""
    if fn.startswith("../"):
        fn = fn.replace("../", "")
    fn = fn.replace("%20", " ")
    return os.path.exists(fn)


def fix_a_cite(line):
    """Fix a citation for change to directory names"""

    # (In theory this code will only ever be needed once
    #  but is harmless if left in place.)
    # Any link like ](../2.%20 needs to be changed to ](../02.%20
    # ](../5.%20title/5.%20title.md needs fixing too
    # ](1.%20 needs changing to ](01.%20

    for j in range(1, 10):
        new = line.replace("](../" + str(j) + ".%20", "](../0" + str(j) + ".%20")
        if new != line:
            # 2nd occurrence possible
            line = new.replace("/" + str(j) + ".%20", "/0" + str(j) + ".%20")
            dprint("Fixed link in " + line)
        else:
            new = line.replace("](" + str(j) + ".%20", "](0" + str(j) + ".%20")
            if new != line:
                # 2nd occurrence possible
                line = new.replace("/" + str(j) + ".%20", "/0" + str(j) + ".%20")
                dprint("Fixed link in " + line)
    return line


def expand_cites():
    """Look for kramdown-style citations and expand them"""
    global section, contents, file_names, topic_file
    schange = False
    inlit = False
    for i in range(len(section)):
        lchange = False
        line = section[i]

        # Handle changes of directory/file names
        new_line = fix_a_cite(line)
        if new_line != line:
            line = new_line
            lchange = True

        # Check for any OBE drafts
        if "](https://datatracker.ietf.org/doc/draft-" in line:
            dr_name = line.split("/doc/", 1)[1].split(")", 1)[0]
            if not draft_current(dr_name):
                logitw("Replaced or missing draft in " + topic_file + "/" + line)

        newcite = False
        if not inlit and line.startswith("```"):
            inlit = True  # start of literal text - ignore
            continue
        if inlit:
            if line.startswith("```"):
                inlit = False  # end of literal text - stop ignoring
            continue
        try:
            if line.count("{{{") != line.count("}}}"):
                logitw("Malformed reference in " + topic_file + "/" + line)
            # convert {{ }} to \[{{ }}\]
            line = line.replace("{{{", "{?x{").replace("}}}", "}?y}")
            line = line.replace("{{", "\[{{").replace("}}", "}}\]")
            line = line.replace("{?x{", "{{").replace("}?y}", "}}")
            if line.count("{{") != line.count("}}"):
                logitw("Malformed reference in " + topic_file + "/" + line)
            while "{{" in line and "}}" in line:
                # dprint("Citation  in:", line)
                # found an expandable citation
                head, body = line.split("{{", maxsplit=1)
                bracketed = head.endswith("\[")
                newcite = True
                cite, tail = body.split("}}", maxsplit=1)
                if (
                    cite.startswith("RFC")
                    or cite.startswith("BCP")
                    or cite.startswith("STD")
                ):
                    if "#" in cite and cite.startswith("RFC"):
                        citen, hasht = cite.split("#")  # separate hashtag
                    else:
                        citen = cite
                        hasht = ""
                    if topic_file != "RFC bibliography":
                        if not rfc_ok(citen):
                            logitw(citen + " not found on line")
                    if not hasht:
                        cite = (
                            "["
                            + cite
                            + "](https://www.rfc-editor.org/info/"
                            + cite.lower()
                            + ")"
                        )
                    else:
                        # special case for section citation
                        cite = (
                            "["
                            + citen
                            + "](https://www.rfc-editor.org/rfc/"
                            + citen.lower()
                            + ".html#"
                            + hasht
                            + ")"
                        )
                    if not bracketed:
                        # citation in noun form
                        cite = (
                            cite.replace("RFC", "RFC ")
                            .replace("BCP", "BCP ")
                            .replace("STD", "STD ")
                        )
                    line = head + cite + tail
                    lchange = True
                elif cite.startswith("I-D."):
                    draft_name = cite[4:]
                    cite = (
                        "["
                        + cite
                        + "](https://datatracker.ietf.org/doc/draft-"
                        + draft_name
                        + "/)"
                    )
                    if not draft_ok(draft_name):
                        logitw(draft_name + " not found on line")
                    line = head + cite + tail
                    lchange = True
                elif cite.startswith("draft-"):
                    draft_name = cite[6:]
                    if not draft_ok(draft_name):
                        logitw(cite + " not found on line")
                    cite = (
                        "[" + cite + "](https://datatracker.ietf.org/doc/" + cite + "/)"
                    )
                    line = head + cite + tail
                    lchange = True

                elif cite[0].isdigit():
                    # print("Found chapter?", cite)
                    found_c = False
                    # extract chapter number
                    if ". " in cite:
                        cnum, sname = cite.split(". ", maxsplit=1)
                        # derive chapter name
                        for cline in contents:
                            if "[" + cnum + "." in cline:
                                chap = cline.split("(")[1].split("/")[0]
                                if cite == chap.replace("%20", " "):
                                    fn = (
                                        "../"
                                        + chap
                                        + "/"
                                        + chap.replace(" ", "%20")
                                        + ".md"
                                    )
                                else:
                                    fn = (
                                        "../"
                                        + chap
                                        + "/"
                                        + sname.replace(" ", "%20")
                                        + ".md"
                                    )
                                if not file_ok(fn):
                                    logitw('"' + cite + '" not found')
                                cite = "[" + cite + "](" + fn + ")"
                                line = head + cite + tail
                                lchange = True
                                found_c = True
                                break
                    if not found_c:
                        # Bogus chapter number
                        line = head + "[" + cite + "](TBD)" + tail
                        lchange = True
                        logitw('"' + cite + '" reference could not be resolved.')

                else:
                    # maybe it's a section name
                    # print("Found section?", cite)
                    if cite in file_names:
                        cite = "[" + cite + "](" + cite.replace(" ", "%20") + ".md)"
                        line = head + cite + tail
                        lchange = True
                    else:
                        # print("Found nothing")
                        line = head + "[" + cite + "](TBD)" + tail
                        lchange = True
                        logitw('"' + cite + '" reference could not be resolved.')
        except:
            # malformed line, do nothing
            logitw("Malformed line in " + topic_file + "/" + line)

        # string bracketed citations together
        if newcite and ")\]" in line:
            line = line.replace(")\]\[", "), ")
            line = line.replace(")\] \[", "), ")
            line = line.replace(")\], \[", "), ")
            line = line.replace(")\],\[", "), ")
            lchange = True

        if lchange:
            section[i] = line
            schange = True

    return schange


######### Startup

# Define some globals

printing = False  # True for extra diagnostic prints
base = []  # the base file for each chapter
base_names = []  # the section names extracted from the base file
warnings = 0  # counts warnings in the log file
written = 0  # counts files written
default_text = "If you know what should be written here, please write it! [How to contribute.](https://github.com/becarpenter/book6/blob/main/1.%20Introduction%20and%20Foreword/How%20to%20contribute.md#how-to-contribute)"

# Horrible hack to avoid spurious 403 errors on redirected URLs
# - we pretend to be a browser. Thank you StackOverflow!

headers = {}
_s = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers["User-Agent"] = _s

# Ensure certificates available. Again, thank you StackOverflow!

# print("CA file", certifi.where())
context = ssl.create_default_context(cafile=certifi.where())


# Has the user supplied a directory on the command line?

cmd_line = False
if len(sys.argv) > 1:
    # user provided directory name?
    if os.path.isdir(sys.argv[1]):
        # assume user has provided directory
        # and set all options to defaults
        os.chdir(sys.argv[1])
        cmd_line = True

# Announce
if not cmd_line:
    Tk().withdraw()  # we don't want a full GUI

    T = "Book reconciler and link maker."

    printing = askyesno(title=T, message="Diagnostic printing?")

    os.chdir(askdirectory(title="Select main book directory"))

# Open log file

flog = open("makeBook.log", "w", encoding="utf-8")
logit("makeBook run at " + time.strftime("%Y-%m-%d %H:%M:%S UTC%z", time.localtime()))

logit("Running in directory " + os.getcwd())

formatting = False
if not formatter:
    logitw("No markdown formatting (mdformat not imported)")
else:
    if cmd_line:
        formatting = False
    else:
        formatting = askyesno(
            title=T,
            message="Rarely needed option!\nRun md formatter on all files?",
            default="no",
        )
if formatting:
    logit("User requested mdformat on all files.")

show("Will read in current contents and RFC index.\nTouch no files until done!")

# Can we check RFCs?
fp = "rfc-index.xml"
rfcs_checkable = True
if (not os.path.exists(fp)) or (time.time() - os.path.getmtime(fp) > 60 * 60 * 24 * 30):
    # need fresh copy of index
    try:
        if cmd_line or askyesno(
            title=T, message="OK to download RFC index?\n(15 MB file)"
        ):
            response = requests.get("https://www.rfc-editor.org/rfc/rfc-index.xml")
            open(fp, "wb").write(response.content)
            logit("Downloaded and cached RFC index")
        else:
            rfcs_checkable = False
    except Exception as E:
        logitw("Cannot get RFC index: " + str(E))
        rfcs_checkable = False
if rfcs_checkable:
    # build dictionary from RFC index
    xf = open(fp, "r", encoding="utf-8", errors="replace")
    index_dict = xmltodict.parse(xf.read())
    xf.close()
    # build lists of BCPs, RFCs and STDs
    all_bcps = index_dict["rfc-index"]["bcp-entry"]
    all_rfcs = index_dict["rfc-index"]["rfc-entry"]
    all_stds = index_dict["rfc-index"]["std-entry"]
    # build list of OBE I-Ds
    all_ids = []
    for e in all_rfcs:
        try:
            all_ids.append(e["draft"][:-3])
        except:
            pass
else:
    logitw("Cannot check RFC existence on-line")

drafts_checkable = url_ok("https://bib.ietf.org")
if not drafts_checkable:
    logitw("Cannot check drafts' existence on-line")

### For testing on-line existence checks
##print("RFC8200:",rfc_ok("RFC8200"))
##print("RFC711:",rfc_ok("RFC711"))
##print("RFC9999:",rfc_ok("RFC9999"))
##print("RFC12345:",rfc_ok("RFC12345"))
##print("BCP97:",rfc_ok("BCP97"))
##print("BCP9876:",rfc_ok("BCP9876"))
##print("STD24:",rfc_ok("STD24"))
##print("STD9875:",rfc_ok("STD9875"))


######### Read previous contents

contents = rf("Contents.md")

######### Scan contents and decorate any plain chapter headings

# Get rid of blank lines in the working copy
contents[:] = (l for l in contents if l.strip(" ") != "\n")

for i in range(len(contents)):
    l = contents[i]
    if l[0].isdigit():
        # Found a plain chapter title - change to link format
        l = l[:-1]  # remove newline
        try:
            _, _ = l.split(" ", maxsplit=1)
        except:
            if not askokcancel(
                title=T, message="Suspect chapter title: " + l + "\nOK to continue?"
            ):
                crash(l + ": bad chapter title, abandoned make")
        url_frag = l.replace(" ", "%20")
        l = "[" + l + "](" + url_frag + "/" + url_frag + ".md)\n"
        contents[i] = l
    elif l.startswith("* ["):
        # Found a contents entry with a link; simplify to plain name
        l, _ = l.split("]", maxsplit=1)
        contents[i] = l.replace("[", "") + "\n"

######### Scan contents and create any missing directories,
######### build chapter list, extract sections lists

chapters = []

contentx = -1  # Note that contents may expand or contract
while contentx < len(contents) - 1:  # dynamically, so we control the loop count
    contentx += 1  # explicitly as we go.
    cline = contents[contentx]
    if cline[0] == "[" and cline[1].isdigit():
        # Found a decorated chapter title - extract chapter name
        cname = cline.split("(")[1].split("/")[0].replace("%20", " ")

        if cname[1] == ".":
            # Single digit chapter name, need to fix it.
            # (In theory this code will only ever be needed once
            #  but is harmless if left in place.)
            logit("Found old chapter name " + cname)
            # Set directory name
            dname = "0" + cname
            # Need to rename directory and base file
            if os.path.isdir(cname):
                # old directory name detected
                os.rename(cname, dname)
                logit("Renamed directory as " + dname)
            if os.path.isfile(dname + "/" + cname + ".md"):
                # old file name detected
                os.rename(dname + "/" + cname + ".md", dname + "/" + dname + ".md")
                logit("Renamed file as " + dname)
        else:
            dname = cname

        chapters.append(dname)

        # Need to create directory?
        if not os.path.isdir(dname):
            os.mkdir(dname)  # create empty directory
            logit("Created directory " + dname)
            # create base file
            base = []
            base.append("# " + cname + "\n\n")
            base.append("General introduction to this chapter.\n\n")
            base.append(default_text + "\n\n")
            base.append("<!-- ## Name (add plain section names like that) -->\n\n")
            base.append(link_warn)
            base.append("### [<ins>Back to main Contents</ins>](../Contents.md)\n")
            wf(dname + "/" + dname + ".md", base)
        else:
            # read the base file
            base = rf(dname + "/" + dname + ".md")
            logit("Processing '" + dname + "'")

        base_changed = False

        # Does the base end with the contents link?
        if not "### [<ins>Back to main" in base[-1]:
            base.append(link_warn)
            base.append("### [<ins>Back to main Contents</ins>](../Contents.md)\n")
            base_changed = True

        # extract section names from base file
        make_basenames()

        # extract section names for existing files
        file_names = []

        for fname in os.listdir(dname):
            if os.path.isfile(os.path.join(dname, fname)):
                if (
                    ".md" in fname
                    and fname[-3:] == ".md"
                    and fname[:-3].lower() != dname.lower()
                ):
                    file_names.append(fname[:-3])
        dprint("Files", file_names)

        # replace section names in Contents.md
        # (it doesn't matter whether they've changed, the list will
        # end up current)

        # N.B. loop within loop on contents list
        contentx += 1
        while contentx < len(contents):
            cline = contents[contentx]
            if contents[contentx].startswith("* "):
                # found a section name to remove
                del contents[contentx]
            else:
                if cline.startswith("[") and cline[1].isdigit():
                    # this must be the next chapter, we'll need the link later
                    _, nextch = cline.split("(", maxsplit=1)
                    nextch = "../" + nextch.replace(".md)\n", "")
                else:
                    nextch = None
                break
        # old sections have gone, contentx points where the
        # new sections belong.

        # Insert section names and links in contente
        for sname in base_names:
            # Note that this assumes no file name case discrepancies
            link = dname + "/" + sname + ".md)"
            link = link.replace(" ", "%20")
            link = "[" + sname + "](" + link
            contents[contentx:contentx] = ["* " + link + "\n"]
            contentx += 1
        contentx -= 1  # so that the outer loop search doesn't skip a line

        # Maybe update base_names
        if base_changed:
            make_basenames()

        # Make uncased versions for comparisons
        u_base_names = uncase(base_names)
        u_file_names = uncase(file_names)

        if set(base_names) != set(file_names):
            # reconciliation needed
            logit("Reconciling base and files for '" + dname + "'")

            # Create a dictionary in case of file-name case discrepancies
            fndict = {}

            # Look for discrepant or missing filenames
            for topic in file_names:
                if (not topic in base_names) and topic.lower() in u_base_names:
                    # we have a file-name case discrepancy
                    logitw(
                        "File-name case discrepancy for '" + dname + "/" + topic + "'"
                    )
                    fndict[topic.lower()] = topic
                elif not topic in base_names:
                    # found a new topic
                    logit("New section '" + topic + "' added to base '" + dname + "'")
                    new_sec = (
                        "\n## [" + topic + "](" + topic.replace(" ", "%20") + ".md)\n"
                    )
                    for bx in range(len(base)):
                        if "### [<ins>Back" in base[bx]:
                            base[bx - 1 : bx - 1] = [new_sec]
                            base_changed = True
                            break

                    logitw(
                        "Run makeBook again to update main contents with new section"
                    )

            # Maybe update base_names
            if base_changed:
                make_basenames()
                u_base_names = uncase(base_names)

            # Look for runt sections in base and create files
            for topic in base_names:
                if not topic.lower() in u_file_names:
                    # There is no file, make it
                    new_md = []
                    new_md.append("## " + topic + "\n\n")
                    new_md.append(default_text + "\n\n")
                    new_md.append(link_warn)
                    new_md.append(link_text("PREVIOUS", "NEXT", dname))
                    wf(dname + "/" + topic + ".md", new_md)
                    # Add link to file in base
                    for bx in range(len(base)):
                        if "## " + topic in base[bx]:
                            base[bx] = (
                                "## ["
                                + topic
                                + "]("
                                + topic.replace(" ", "%20")
                                + ".md)\n"
                            )
                            base_changed = True
                            break
                    # Add file name
                    file_names.append(topic)
                    u_file_names = uncase(file_names)

        if base_changed or formatting:
            wf(dname + "/" + dname + ".md", base)

        # Now fixup link lines in section files. The only safe way
        # is to read them all and write back if fixed.

        # Assertion: base names and file names now match except for any case discrepancies

        if set(u_base_names) != set(u_file_names):
            dprint(dname, "Base names", base_names)
            dprint(dname, "File names", file_names)
            crash("Fatal base and file names mismatch in '" + dname + "'")

        # The sections are by definition in the order shown in the chapter base

        # Make a list of file names sorted like the base names
        # (Necessary because of possible case discrepancies)
        sorted_file_names = []
        for topic in base_names:
            try:
                # get actual file name from dictionary
                sorted_file_names.append(fndict[topic.lower()])
            except:
                # not in dictionary, so no case discrepancy
                sorted_file_names.append(topic)

        # Make the link line for each section
        # and update section file if necessary.
        # Also expand "kramdown" citations.
        for bx in range(len(base_names)):
            topic = base_names[bx]
            topic_file = sorted_file_names[bx]
            # is there a previous  topic?
            if bx == 0:
                previous = None
            else:
                previous = sorted_file_names[bx - 1]
            # is there a subsequent topic?
            if bx == len(base_names) - 1:
                nxt = nextch  # link to next chapter, if available
            else:
                nxt = sorted_file_names[bx + 1]
            link_line = link_text(previous, nxt, dname)

            section = rf(dname + "/" + topic_file + ".md")
            section_changed = expand_cites()
            if "### [<ins>" in section[-1]:
                # replace existing link line if necessary
                if section[-1].strip("\n") != link_line:
                    section[-1] = link_line
                    section_changed = True
            else:
                # add new link line
                section.append(link_warn)
                section.append(link_line)
                section_changed = True

            if section_changed or formatting:
                wf(dname + "/" + topic_file + ".md", section)

        # Expand citations for chapter base file itself
        section = rf(dname + "/" + dname + ".md")
        topic_file = dname  # used by expand_cites()
        if expand_cites() or formatting:
            wf(dname + "/" + dname + ".md", section)

######### Rewrite contents

# ensure there is a blank line before each link or # title
# and that logo is followed by blank line
for i in range(1, len(contents)):
    fixed = fix_a_cite(contents[i])
    if fixed != contents[i]:
        contents[i] = fixed
    if contents[i].startswith("[") or contents[i].startswith("#"):
        contents[i] = "\n" + contents[i]
    elif contents[i].startswith("<img src="):
        contents[i] += "\n"

# and write it back
wf("Contents.md", contents, mdf=False)


######### Close log and exit

flog.close()

if warnings:
    warn = str(warnings) + " warning(s)\n"
else:
    warn = ""

if written:
    wrote = str(written) + " file(s) written.\n"
else:
    wrote = "Clean run.\n"

show(wrote + warn + "Check makeBook.log.")

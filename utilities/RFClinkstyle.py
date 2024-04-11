#!/usr/bin/env python3

# I've noticed RFC link styles like the following with varying spacing and brackets
# RFC1234 , [RFC1234], RFC 1234, and [RFC 1234]
# @buraglio suggests standardizing on [RFC1234]
# This isn't perfect so verify the output.
#
# Point this script at a directory and it will read all *.md files and attempt to 
# format all RFC links to the same style.
# Usage: python3 ./utilities/RFClinkstyle.py 1.\ Introduction\ and\ Foreword

import sys
import os
import re

if not os.path.isdir(sys.argv[1]):
    print("Gonna need a directory.")
    exit()

files = os.listdir(sys.argv[1])

# 1. This will not attempt to fix style where there is more than an RFC plus a number between the brackdes
# 2. a leading \[ or trailing \] are both optionally in the doc now, usually when the RFC
# is listed as a reference vs in-line in the text.

# bracket usage varies
# RFC1234  <- we assume in-line text, it's fine
# [RFC1234 <- needs fixed
# RFC1234]  <- needs fixed
# [RFC1234] <- assume reference, it's fine
# [RFC1234, RFC5678]  <- list of references, fine
# [RFC1234], [RFC5678]  <- list of references, needs fixed.

# ah dang!  I forgot about cases where we list multiple RFCs separated by commas, but even that isn't
# consistently done.  So we actually move to the [RFC1234], [RFC5678] version first,
# then fix it later.

rfc_re = re.compile(r'((\\\[)?\[\s*RFC\s*(\d+)\s*\]\(([^)]*rfc-editor[^\)]+)\)(\\\])?)')
brackets_re = re.compile(r'\)(?:\\\])?,(\s+)(?:\\\[)?\[RFC')

for f in files:
    print("Processing ",f)
    if(f.endswith(".md")):
        myfile = sys.argv[1] + "/" + f
        contents = open(myfile,"r").read().splitlines()
        rewrite_file = False

        # we do line-by-line because the same RFC is sometimes referenced in a file more than once
        for i in range(len(contents)):

            res = rfc_re.findall(contents[i])
            for m in res:
                actual = m[0] # full pattern match
                rfc = m[2]
                url = m[3]
                brackets = False
                if(m[1] == "\[" or m[4] == "\]"):
                    brackets = True

                # the correct line per our style:
                correct = "[RFC" + rfc + "](" + url + ")"
                if(brackets):
                    correct = "\[" + correct + "\]"
                if(actual != correct):
                    print("Actual:",actual)
                    print("Correct:",correct)
                    contents[i] = contents[i].replace(actual,correct)

        all_contents = "\n".join(contents) + "\n"
        # now that we're all back together we can fix the lists
        all_contents = brackets_re.sub(r'),\1[RFC', all_contents)

        print("Writing ",myfile)
        with open(myfile,"w") as outfile:
            outfile.write(all_contents)




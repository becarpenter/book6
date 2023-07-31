#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build IPv6 RFC bibliography"""

# Version: 2023-05-23 - original
# Version: 2023-07-29 - check age of index
# Version: 2023-07-31 - added STD/BCP numbers;
#                       caught more RFCs; cosmetics


########################################################
# Copyright (C) 2023 Brian E. Carpenter.                  
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

def logit(msg):
    """Add a message to the log file"""
    global flog, printing
    flog.write(msg+"\n")
    if printing:
        print(msg)
        
def logitw(msg):
    """Add a warning message to the log file"""
    global warnings
    logit("WARNING: "+msg)
    warnings += 1

def dprint(*msg):
    """ Diagnostic print """
    global printing
    if printing:
        print(*msg)

def crash(msg):
    """Log and crash"""
    printing = True
    logit("CRASH "+msg)
    flog.close()
    exit() 

def rf(f):
    """Return a file as a list of strings"""
    file = open(f, "r",encoding='utf-8', errors='replace')
    l = file.readlines()
    file.close()
    #ensure last line has a newline
    if l[-1][-1] != "\n":
        l[-1] += "\n"
    return l

def wf(f,l):
    """Write list of strings to file"""
    file = open(f, "w",encoding='utf-8')
    for line in l:
        file.write(line+"\n")
    file.close()
    logit("'"+f+"' written")

def field(fname, block):
    """Extract named field from XML block"""
    _,temp = block.split("<"+fname+">", maxsplit=1)
    result,_ = temp.split("</"+fname+">", maxsplit=1)
    return result
    

def title(block):
    """Extract title from XML block"""
    return field("title", block)

def doc_id(block):
    """Extract doc-id from XML block"""
    return field("doc-id", block)
    

def interesting(block):
    """Save interesting RFC data from XML block"""
    global stds, bcps, infos, exps
    
    if "UNKNOWN" in block:
        return None
    elif "<current-status>HISTORIC" in block:
        return False
    elif "<obsoleted-by>" in block:
        return False
    elif "IPv6" in title(block) or "IP Version 6" in title(block):
        #print(block)
        status = field("current-status", block)
        if "is-also" in block:
            also,_ = field("is-also", block).split("<doc-id>")[1].split("</")
            if also.startswith("BCP0"):
                also = "BCP"+also[3:].lstrip("0")
            elif also.startswith("STD0"):
                also = "STD"+also[3:].lstrip("0")
            also = " ({{{"+also+"}}})"
        else:
            also = ""
        #print(also)
        if "STANDARD" in status:
            stds.append("- {{{"+doc_id(block)+"}}}"+also+": "+title(block))
        elif status == "BEST CURRENT PRACTICE":
            bcps.append("- {{{"+doc_id(block)+"}}}"+also+": "+title(block))
        elif status =="INFORMATIONAL":
            infos.append("- {{{"+doc_id(block)+"}}}: "+title(block))
        elif status == "EXPERIMENTAL":
            exps.append("- {{{"+doc_id(block)+"}}}: "+title(block))
        else:
            logitw("Unclassified:\n"+block)
        return True
    return False

######### Startup

#Define some globals

inrfc = False
new = ''
numberfound = False
count = 0
stds = []
bcps = []
infos= []
exps = []
printing = False # True for extra diagnostic prints
warnings = 0

#Announce

Tk().withdraw() # we don't want a full GUI

T = "IPv6 RFC bibliography maker."

printing = askyesno(title=T,
                    message = "Diagnostic printing?")

where = askdirectory(title = "Select main book directory")
                   
os.chdir(where)

#Open log file

flog = open("RFCbib6.log", "w",encoding='utf-8')
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())
logit("RFCbib6 run at "+timestamp)

logit("Running in directory "+ os.getcwd())


showinfo(title=T,
         message = "Will read complete RFC bibliography.\nTouch no files until done!")
try:
    path = "C:/brian/docs/IETF stuff/rfc/rfc-index.xml"
    if time.time()-os.path.getmtime(path) > 60*60*24*30:
        logitw("rfc-index.xml is >30 days old")
    whole = rf(path)
except:
    try:
        if askyesno(title=T, message = "OK to download RFC index?/n(15 MB temp file)"):
            import urllib.request
            urllib.request.urlretrieve("http://www.rfc-editor.org/rfc/rfc-index.xml", "tempRx.xml")
            whole = rf("tempRx.xml")
            os.remove("tempRx.xml")
        else:
            crash("Cannot run without RFC index")
    except:
        crash("rfc-index.xml not found")
    
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())

for line in whole:
    #print(line)
    if (not inrfc) and (not "<rfc-entry>" in line):
        continue
    inrfc = True
    new += line
    if inrfc and "</rfc-entry>" in line:
        #end of an rfc entry
        if interesting(new):         
            count += 1
        inrfc = False
        numberfound = False
        new = ''
        continue
    
logit(str(count)+" IPv6 RFCs found")
if len(stds)+len(bcps)+len(infos)+len(exps) != count:
    logitw("Warning: count mismatch")

md = ["## RFC bibliography","",
      """This section is a machine-generated list of all current RFCs that mention
IPv6 in their title. Obsolete RFCs are not included. There are subsections for
Standards, BCPs, Informational and Experimental RFCs. Be *cautious* about old
Informational or Experimental RFCs - they may be misleading as well as out of date."""]
md += ["","RFCbib6 run at "+timestamp]
md += ["","### Standards Track",""]
md += stds
md += ["", "### Best Current Practice", ""]
md += bcps
md += ["", "### Informational", ""]
md += infos
md += ["", "### Experimental", ""]
md += exps
md += ["", "<!-- Link lines generated automatically; do not delete -->",
       "### [<ins>Chapter Contents</ins>](20.%20Further%20Reading.md)"]

wf("20. Further Reading/RFC bibliography.md", md)

######### Close log and exit
    
flog.close()

if warnings:
    warn = str(warnings)+" warning(s)\n"
else:
    warn = ""

showinfo(title=T,
         message = warn+"Check RFCbib6.log, then run makeBook.")
    

    

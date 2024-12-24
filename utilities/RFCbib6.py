#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build IPv6 RFC bibliography"""

# Version: 2023-05-23 - original
# Version: 2023-07-29 - check age of index
# Version: 2023-07-31 - added STD/BCP numbers;
#                       caught more RFCs; cosmetics
# Version: 2023-08-01 - catch by WG acronym;
#                       display counts
# Version: 2023-08-10 - download & cache xml index
# Version: 2024-04-28 - handle directory on command line;
#                       catch DHCPv6
# Version: 2024-04-28 - tiny bug in crash()
# Version: 2024-11-16 - add citation of chapter 10
# Version: 2024-11-24 - corrected citation of chapter 10
# Version: 2024-12-24 - switch to proper xml parser

########################################################
# Copyright (C) 2023-24 Brian E. Carpenter.                  
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
import requests
import xmltodict

def show(msg):
    """Show a message"""
    global T, cmd_line
    if cmd_line:
        print(msg)
    else:
        showinfo(title=T, message = msg)

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
    global printing
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
    try:
        return block[fname]
    except:
        return None      

def title(block):
    """Extract title from XML block"""
    return field("title", block)

def doc_id(block):
    """Extract doc-id from XML block"""
    return field("doc-id", block)  

def interesting(block):
    """Save interesting RFC data from XML block"""
    global stds, bcps, infos, exps
    status = block['current-status']
    if status in ["UNKNOWN", "HISTORIC"]:
        return False
    elif field("obsoleted-by", block):
        return False
    elif ("IPv6" in block['title'] or "IP Version 6" in block['title'] or "DHCPv6" in block['title']
          or (field("wg_acronym", block) in wgs)):
        #print(block)
        status = block["current-status"]
        if field("is-also", block):
            also = block["is-also"]["doc-id"]
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
wgs = ["6man","v6ops"]

#Has the user supplied a directory on the command line?

cmd_line = False
if len(sys.argv) > 1:
    #user provided directory name?
    if os.path.isdir(sys.argv[1]):
        #assume user has provided directory
        #and set all options to defaults
        os.chdir(sys.argv[1])
        cmd_line = True

#Announce
if not cmd_line:
    Tk().withdraw() # we don't want a full GUI

    T = "IPv6 RFC bibliography maker."

    printing = askyesno(title=T,
                        message = "Diagnostic printing?")

    os.chdir(askdirectory(title = "Select main book directory"))
                   


#Open log file

flog = open("RFCbib6.log", "w",encoding='utf-8')
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())
logit("RFCbib6 run at "+timestamp)

logit("Running in directory "+ os.getcwd())


show("Will read complete RFC index.\nTouch no files until done!")

fp = "rfc-index.xml"
if (not os.path.exists(fp)) or (time.time()-os.path.getmtime(fp) > 60*60*24*30):
    #need fresh copy of index
    try:
        if cmd_line or askyesno(title=T, message = "OK to download RFC index?\n(15 MB file)"):
            response = requests.get("https://www.rfc-editor.org/rfc/rfc-index.xml")
            open(fp, "wb").write(response.content)
            logit("Downloaded and cached RFC index")
        else:
            raise Exception("Invalid choice")
    except Exception as E:
        logitw(str(E))
        crash("Cannot run without RFC index")
xf = open(fp,"r",encoding='utf-8', errors='replace')
index_dict = xmltodict.parse(xf.read())
xf.close()
all_rfcs = index_dict['rfc-index']['rfc-entry']
  
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())

for r in all_rfcs:
    if interesting(r):         
        count += 1
    
logit(str(count)+" IPv6 RFCs found")
if len(stds)+len(bcps)+len(infos)+len(exps) != count:
    logitw("Warning: count mismatch")

md = ["## RFC bibliography","",
      """This section is a machine-generated list of all current RFCs that
mention IPv6 or DHCPv6 in their title or come from the major IPv6 working groups.
Obsolete RFCs are not included. There are subsections for Standards, BCPs, 
Informational and Experimental RFCs. Be *cautious* about old Informational
or Experimental RFCs - they may be misleading as well as out of date. Also see
[10. Obsolete Features in IPv6](../10.%20Obsolete%20Features%20in%20IPv6/10.%20Obsolete%20Features%20in%20IPv6.md)."""]
md += ["","RFCbib6 run at "+timestamp+" ("+str(count)+" RFCs found)"]
md += ["","### Standards Track ("+str(len(stds))+" RFCs)",""]
md += stds
md += ["", "### Best Current Practice ("+str(len(bcps))+" RFCs)", ""]
md += bcps
md += ["", "### Informational ("+str(len(infos))+" RFCs)", ""]
md += infos
md += ["", "### Experimental ("+str(len(exps))+" RFCs)", ""]
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

show(warn+"Check RFCbib6.log, then run makeBook.")
    

    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Clean up RFC cites to match RFC-Editor style"""

# Version: 2024-05-13 - original

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
import sys
import os

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


def wf(f,l, mdf = True):
    """Write list of strings to file"""
    global written
    file = open(f, "w",encoding='utf-8')
    for line in l:
        file.write(line)
    file.close()
    logit("'"+f+"' written")
    written +=1 

   

def fix_cites(section):
    """Look for RFC citations and fix them if needed"""
    global changes
    schange = False
    inlit = False
    for i in range(len(section)):
        lchange = False
        line = section[i]
        newcite = False
        if not inlit and line.startswith("```"):
            inlit = True    #start of literal text - ignore
            continue
        if inlit:
            if line.startswith("```"):
                inlit = False   #end of literal text - stop ignoring
            continue
            
        ## Transform needed:
        ##'\[[RFC' no change
        ##'\[[BCP' no change
        ##'\[[STD' no change
        ##'[RFC '  no change
        ##'[BCP '  no change
        ##'[STD '  no change
        ##'[RFC'   -> '[RFC '
        ##'[BCP'   -> '[BCP '
        ##'[STD'   -> '[STD '

        c = 0
        while c < len(line)-6:
            if line[c:].startswith("\[["):
                c += 6
            elif line[c:].startswith("[RFC ") or line[c:].startswith("[BCP ") or line[c:].startswith("[STD "):
                c += 5
            elif line[c:].startswith("[RFC") or line[c:].startswith("[BCP") or line[c:].startswith("[STD"):
                if line[c+4].isdigit():
                    line = line[:c+4] + " " + line[c+4:]
                    lchange = True
                c += 5
            else:
                c += 1
                           
        if lchange:
            changes += 1
            dprint("Changed\n", section[i], "to\n", line)
            section[i] = line
            schange = True
            
    if schange:
        return section
    else:
        return False

######### Startup

#Define some globals

printing = False # True for extra diagnostic prints
warnings = 0     # counts warnings in the log file
changes = 0      # counts citations changed
written = 0      # counts files written


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

    T = "Cite fixer."

    if not askyesno(title=T,
                    message = "Rarely needed program. Are you sure?",
                    default = 'no'):
        exit()

    printing = askyesno(title=T,
                        message = "Diagnostic printing?")

    os.chdir(askdirectory(title = "Select main book directory"))
                   
#Open log file

flog = open("fixCites.log", "w",encoding='utf-8')
logit("fixCites run at "
      +time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime()))

logit("Running in directory "+ os.getcwd())

show("Will read in everything.\nTouch no files until done!")

######### Scan all .md files in subdirectories

for path, subdirs, files in os.walk('.'):
    path = path.replace('\\','/')
    if path.startswith('./') and path[2].isdigit():                   
        dprint("Processing directory", path)
        for fn in files:
            if fn.endswith('.md') and not "RFC bibliography" in fn:
                dprint("Processing file", fn)
                changed = fix_cites(rf(path+'/'+fn))
                if changed:
                    wf(path+'/'+fn, changed)                    
             
######### Close log and exit
    
flog.close()

if warnings:
    warn = str(warnings)+" warning(s)\n"
else:
    warn = ""

if changes:
    chst = str(changes)+" citation(s) changed\n"
else:
    chst = ""

if written:
    wrote = str(written)+" file(s) written.\n"
else:
    wrote = "Clean run.\n"

show(chst+wrote+warn+"Check fixCites.log.")


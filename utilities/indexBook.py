#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a book6 index"""

# Version: 2022-12-26 - original
# Version: 2022-12-27 - cosmetic improvements
# Version: 2022-12-28 - allow keywords starting with digit
# Version: 2022-12-30 - include timestamp
# Version: 2023-01-02 - added alt text to logo
# Version: 2023-01-03 - added Contents link at end of index
# Version: 2023-01-05 - added citation index
# Version: 2023-01-10 - added warnings of invalid internal citations
# Version: 2023-05-20 - exclude RFC bibliography from indexing
# Version: 2023-11-01 - enhance index boilerplate


########################################################
# Copyright (C) 2022-2023 Brian E. Carpenter.                  
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
    """Return a file as a list of lower case strings"""
    file = open(f, "r",encoding='utf-8', errors='replace')
    l = file.readlines()
    file.close()
    return l

def file_ok(fn):
    """Check if a local file is OK"""
    if fn.startswith("../"):
        fn = fn.replace("../","")
    fn = fn.replace("%20"," ")
    return os.path.exists(fn)


def wf(f,l):
    """Write list of strings to file"""
    global written
    file = open(f, "w",encoding='utf-8')
    for line in l:
        file.write(line)
    file.close()
    logit("'"+f+"' written")
 

def uncase(l):
    """Return lower case version of a list of strings"""
    u = []
    for s in l:
        u.append(s.lower())
    return u

specials = ('-','$')    #characters allowed in index terms (as well as letters and digits)
ignores = ('and', 'the', 'but', 'for', 'not', 'are', 'all', 'new', 'was', 'can', 'may', 'one',
           'two', 'has', 'out', 'use', 'any', 'see', 'now', 'get', 'how', 'its', 'top', 'had',
           'that', 'then')

def good(word):
    """Is the word useful?"""
    if word in ignores:
        return False
    return len(word)>2

def exwords(target):
    """Return list of words in a target list of strings"""
    words = []
    for line in target:
        line = line.lower()
        if line.strip().startswith('<!--') or line.strip().endswith('-->'):
            continue #best effort to remove XML comments
        if line.startswith('## [') or line.startswith('### ['):
            continue #remove section links
        inspace = False
        inword = False
        #hack to combine multi-word terms
        for item in split_terms:
            if item in line:
                line = line.replace(item, item.replace(' ','$'))
        for c in ' '+line: #scan characters
            if c == ' ':
                inspace = True
                if not inword:                    
                    continue
                else:
                    #end of word
                    if good(word):
                        words.append(word)
                    inword = False
            elif c.islower() or c.isdigit() or c in specials:
                inspace = False
                if inword:
                    word += c
                else:
                    word = c
                    inword = True
            else:   #neither space nor letter nor digit nor special
                if inword:  #treat as end of word
                    if good(word):
                        words.append(word)
                    inword = False
    return words

def indexable(word):
    """if word is indexable, return indexing term"""
    for i in range(len(index_terms)):
        terms = index_terms[i].split(' ')
        for term in terms:
            if word == term.lower():
                return index_terms[i]
    return None

def packx(index):
    """Sort and pack an index"""
    index = sorted(index, key=str.casefold)
    same = None
    for i in range(len(index)):
        head = index[i].split("]")[0]
        if head != same:
            index[i-1] += "\n"
            index[i] = index[i].replace(head, head+' '+blob)
            same = head
        else:
            index[i] = index[i].replace(head, '['+blob)
    return index

link_warn = "<!-- Link lines generated automatically; do not delete -->\n"
blob = '●'

######### Startup

#Define some globals

printing = False # True for extra diagnostic prints
warnings = 0

#Announce

Tk().withdraw() # we don't want a full GUI

T = "Book index maker."

printing = askyesno(title=T,
                    message = "Diagnostic printing?")

where = askdirectory(title = "Select main book directory")
                   
os.chdir(where)

#Open log file

flog = open("indexBook.log", "w",encoding='utf-8')
timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())
logit("indexBook run at "+timestamp)

logit("Running in directory "+ os.getcwd())


showinfo(title=T,
         message = "Will read indexing terms and current book6 text.\nTouch no files until done!")



######### Read indexing terms

raw_terms = rf("utilities/index6.txt")
index_terms = []
split_terms = []
for t in raw_terms:
            
    if t.strip() and not t.strip().startswith("#"):
        while "'" in t:
            #hack to combine multi-word terms
            head, split_term, tail = t.split("'", maxsplit=2)
            split_terms.append(split_term.lower())
            t = head+split_term.replace(" ","$")+tail
        index_terms.append(t.strip())
        
dprint("Index terms:", index_terms)
dprint("Split terms:", split_terms)

######### Create empty index and citation index

index = []
citex = []

######### Scan all .md files in subdirectories

for path, subdirs, files in os.walk('.'):
    path = path.replace('\\','/')
    if path.startswith('./') and path[2].isdigit():
        dprint("Processing directory", path)
        for fn in files:
            if fn.endswith('.md') and not "RFC bibliography" in fn:
                dprint("Processing file", fn)
                target = rf(path+'/'+fn)
                #first scan for indexable words and citations
                words = exwords(target)
                url = (path+'/'+fn).replace(' ','%20')
                for w in words:
                    wx = indexable(w)
                    if wx:
                        ##dprint(wx, '===', w)
                        term = wx.split()[0].replace('$',' ')
                        cite = '['+term+']('+url+')\n'
                        if not cite in index:
                            index.append(cite)
                    if w.startswith('rfc') or w.startswith('bcp') or w.startswith('std'):
                        if len(w) < 8 and not w.isalpha():
                            cite = '['+w.upper()+']('+url+')\n'
                            if not cite in citex:
                                citex.append(cite)
                #now scan for invalid internal citations
                #and report errors
                for line in target:
                    #look for internal link pattern like
                    #[2. Addresses](../2.%20IPv6%20Basic%20Technology/Addresses.md)
                    if "](TBD)" in line:
                        logitw("Undefined TBD reference in '"+path[2:]+'/'+fn+"'.")
                    while "](../" in line:
                        _, line = line.split("](../", maxsplit=1)
                        f_cited, line = line.split(")", maxsplit=1)
                        if not file_ok(f_cited):
                            logitw("Invalid reference to '"+f_cited.replace("%20", " ")+"' in '"+path[2:]+'/'+fn+"'.")

index = packx(index)

index.insert(0,'# book6 Main Index\n')
index.insert(1,'<img src="./book6logo.png" alt="book6 logo" width="200px" height="auto"/>\n\n')
index.insert(2,"Generated at "+timestamp+"\n\n")
index.insert(3,"This index was created automatically, so it's dumb. ")
index.insert(4,"It is not case-sensitive. ")
index.insert(5,'It has links to each section that mentions each keyword.\n')
index.insert(6,'If you think any keywords are missing, please raise an issue (use link on GitHub toolbar).\n')
index.insert(7,link_warn)
index.append("\n### [<ins>Back to main Contents</ins>](Contents.md)")
wf("Index.md", index)

citex = packx(citex)

citex.insert(0,'# book6 Citation Index\n')
citex.insert(1,'<img src="./book6logo.png" alt="book6 logo" width="200px" height="auto"/>\n\n')
citex.insert(2,"Generated at "+timestamp+"\n\n")
citex.insert(3,"This index was created automatically, so it's dumb. ")
citex.insert(4,'It has links to each section that mentions each citation.\n')
citex.insert(5,link_warn)
citex.append("\n### [<ins>Back to main Contents</ins>](Contents.md)")
wf("Citex.md", citex)
           
             
######### Close log and exit
    
flog.close()

if warnings:
    warn = str(warnings)+" warning(s)\n"
else:
    warn = ""

showinfo(title=T,
         message = warn+"Check indexBook.log.")


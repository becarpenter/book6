#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a book6 index"""

# Version: 2022-12-26 - original
# Version: 2022-12-27 - cosmetic improvements


########################################################
# Copyright (C) 2022 Brian E. Carpenter.                  
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
    return uncase(l)


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
    return len(word)>2 and not word[0].isdigit()

def exwords(target):
    """Return list of words in a target list of strings"""
    words = []
    for line in target:
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
            if word == term:
                return index_terms[i]
    return None

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
logit("indexBook run at "
      +time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime()))

logit("Running in directory "+ os.getcwd())


showinfo(title=T,
         message = "Will read indexing terms and current book6 text.\nTouch no files until done!")



######### Read indexing terms

raw_terms = rf("utilities/index6.txt")
index_terms = []
split_terms = []
for t in raw_terms:
            
    if t.strip() and not t.strip().startswith("#"):
        if "'" in t:
            #hack to combine multi-word terms
            head, split_term, tail = t.split("'")
            split_terms.append(split_term)
            t = head+split_term.replace(" ","$")+tail
        index_terms.append(t.strip())
        
dprint("Index terms:", index_terms)

######### Create empty index
index = []




######### Scan all .md files in subdirectories


for path, subdirs, files in os.walk('.'):
    path = path.replace('\\','/')
    if path.startswith('./') and path[2].isdigit():
        dprint("Processing directory", path)
        for fn in files:
            if fn.endswith('.md'):
                dprint("Processing file", fn)
                target = rf(path+'/'+fn)
                words = exwords(target)
                for w in words:
                    wx = indexable(w)
                    if wx:
                        ##dprint(wx, '===', w)
                        term = wx.split()[0].replace('$',' ')
                        url = (path+'/'+fn).replace(' ','%20')
                        cite = '['+term+']('+url+')\n'
                        if not cite in index:
                            index.append(cite)
                
index.sort()

same = None

for i in range(len(index)):
    head = index[i].split("]")[0]
    if head != same:
        index[i-1] += "\n"
        index[i] = index[i].replace(head, head+' '+blob)
        same = head
    else:
        index[i] = index[i].replace(head, '['+blob)

index.insert(0,'# book6 Main Index\n')
index.insert(1,"This index was created automatically, so it's dumb. ")
index.insert(2,"It is not case-sensitive. ")
index.insert(3,'It has links to each section that mentions each keyword.\n')
index.insert(4,link_warn)     
wf("Index.md", index)          
           
             
######### Close log and exit
    
flog.close()

if warnings:
    warn = str(warnings)+" warning(s)\n"
else:
    warn = ""

showinfo(title=T,
         message = warn+"Check indexBook.log.")


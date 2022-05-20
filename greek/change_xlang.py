#-*- coding:utf-8 -*-
"""make_change_4.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class Change(object):
 def __init__(self,lnum,line,newline,metaline):
  self.lnum = lnum
  self.line = line
  self.newline = newline
  self.metaline = metaline
  
def write_changes(fileout,changes):
 outrecs=[]
 prevmeta = None
 for change in changes:
  outarr=[]
  lnum = change.lnum
  line = change.line
  newline = change.newline
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  if prevmeta != metaline:
   outarr.append('; --------------------------------------------------')
   outarr.append('; %s' % metaline)
  else:
   outarr.append(';')
  prevmeta = metaline
  outarr.append('%s old %s' %(lnum,line))
  outarr.append('%s new %s' %(lnum,newline))
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"changes written to",fileout)

def make_changes(entries):
 changes = []
 emptygreek = '<lang n="greek"></lang>'
 for ientry,entry in enumerate(entries):
  for iline,line in enumerate(entry.datalines[0:-1]):
   if line.endswith(emptygreek):
    iline1 = iline + 1
    line1 = entry.datalines[iline1]
    if line1.startswith(emptygreek):
     lnum = entry.linenum1 + iline1 + 1
     newline = line1.replace(emptygreek,'<xlang n="greek"></lang>',1)
     metaline = entry.metaline
     change = Change(lnum,line1,newline,metaline)
     changes.append(change)
 return changes

if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileout = sys.argv[2] #  

 entries = digentry.init(filein)
 digentry.Entry.Ldict = {}

 changes = make_changes(entries)
 write_changes(fileout,changes)

 

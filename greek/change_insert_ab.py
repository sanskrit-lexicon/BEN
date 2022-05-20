#-*- coding:utf-8 -*-
"""change_insert_ab.py
 
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
 for change in changes:
  outarr=[]
  lnum = change.lnum
  line = change.line
  newline = change.newline
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  outarr.append('; %s' % metaline)
  outarr.append('%s old %s' %(lnum,line))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,newline))
  outarr.append('; ---------------------------')
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"changes written to",fileout)

def check_entries_L(Ldict,Ldictab):
 s = set(Ldict.keys())
 sab = set(Ldictab.keys())
 diff1 = s.difference(sab)
 print('in L not in Lab',diff1)
 diff2 = sab.difference(s)
 print('in Lab not in L',diff2)

def greek_instances(entry):
 a = []
 for line in entry.datalines:
  b = re.findall(r'<lang n="greek">.*?</lang>',line)
  for x in b:
   a.append(x)
 return a

def make_changes(entries,entriesab):
 changes = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  greeks = greek_instances(entry)
  greeksab = greek_instances(entryab)
  if len(greeks) != len(greeksab):
   print('ERROR at',entry.metaline)
   print('different number of instances: %s != %s' %(len(greeks),len(greeksab)))
   exit(1)
  if len(greeks) == 0:
   continue # nothing to do
  #print(entry.metaline, len(greeks))
  text = '\n'.join(entry.datalines)
  parts = re.split(r'(<lang n="greek"></lang>)',text,flags=re.DOTALL)
  igreek = 0
  newparts = []
  for part in parts:
   if part == '<lang n="greek"></lang>':
    newpart = greeksab[igreek]
    igreek = igreek + 1
   else:
    newpart = part
   newparts.append(newpart)
  if igreek != len(greeks):
   print('dbg: %s != %s' %(igreek,len(greeks)))
   exit(1)
  newtext = ''.join(newparts)
  newlines = newtext.split('\n')
  ##
  assert len(entry.datalines) == len(newlines)
  #print('check',entry.metaline,len(entry.datalines),len(newlines))
  for iline,line in enumerate(entry.datalines):
   newline = newlines[iline]
   if newline == line:
    continue
   # line is changed
   lnum = entry.linenum1 + iline + 1
   metaline = entry.metaline
   change = Change(lnum,line,newline,metaline)
   #print(metaline)
   changes.append(change)
 return changes

if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileab = sys.argv[2] # bop ab
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 digentry.Entry.Ldict = {}
 entriesab = digentry.init(fileab)

 changes = make_changes(entries,entriesab)
 print('len(changes)=',len(changes))
 write_changes(fileout,changes)

 

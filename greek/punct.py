#-*- coding:utf-8 -*-
"""punct.py
 
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

def greek_instances_old(entry):
 a = []
 for line in entry.datalines:
  b = re.findall(r'<lang n="greek">.*?</lang>.',line,flags = re.DOTALL)
  for x in b:
   a.append(x)
 return a

def greek_instances(text):
 a = re.findall(r'<lang n="greek">.*?</lang>.',text,flags = re.DOTALL)
 return a

def langspace(oldlines):
 newlines = []
 for line in oldlines:
  if line.endswith('</lang>'):
   newline = line + ' '
  else:
   newline = line
  newlines.append(newline)
 return newlines

def make_changes(entries,entriesab):
 changes = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  #text = '\n'.join(entry.datalines) + '\n'
  # lines in entry.datalines may end in </lang> (533)
  # lines in entrab.datalines never end in </lang>
  lines = langspace(entry.datalines)
  text = '\n'.join(lines)
  textab = '\n'.join(entryab.datalines)
  greeks = greek_instances(text)
  greeksab = greek_instances(textab)
  if len(greeks) != len(greeksab):
   print('ERROR at',entry.metaline)
   print('different number of instances: %s != %s' %(len(greeks),len(greeksab)))
   exit(1)
  if len(greeks) == 0:
   continue # nothing to do
  #print(entry.metaline, len(greeks))
  #text = '\n'.join(entry.datalines)
  parts = re.split(r'(<lang n="greek">.*?</lang>.)',text,flags=re.DOTALL)
  igreek = 0
  newparts = []
  for part in parts:
   if part.startswith('<lang n="greek">'):
    newpart = greeksab[igreek]
    assert part[0:-1] == newpart[0:-1]
    if newpart != part:
     #print('%s => %s' % (part,newpart))
     if part[-1] == ' ':
      newpart = newpart + ' '
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
   # possibly, newline only differs by having a trailing space
   # don't count these as changes.
   newline = newline.rstrip()
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

 

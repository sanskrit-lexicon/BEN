#-*- coding:utf-8 -*-
"""prep1.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

def check_entries_L(Ldict,Ldictab):
 s = set(Ldict.keys())
 sab = set(Ldictab.keys())
 diff1 = s.difference(sab)
 print('in L not in Lab',diff1)
 diff2 = sab.difference(s)
 print('in Lab not in L',diff2)

def check_metaline(entries,entriesab):
 nprob = 0
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  if entry.metaline != entryab.metaline:
   lnum = entry.linenum1
   print('%s old %s' %(lnum,entry.metaline))
   print('%s new %s' %(lnum,entryab.metaline))
   print(';')
   nprob = nprob + 1
   continue
   # rest of code not needed
   keys = list(entry.metad.keys())
   keysab = list(entryab.metad.keys())
   assert keys == keysab
   diffvals = []
   for key in keys:
    val = entry.metad[key]
    valab = entryab.metad[key]
    if val != valab:
     diffvals.append('%s: %s != %s' %(key,val,valab))
   print(diffvals)
   #print('%s != %s' %(entry.metaline ,entryab.metaline))
   nprob = nprob + 1
 print('check_metaline finds %s differences' % nprob)

def greek_instances(entry):
 a = []
 for line in entry.datalines:
  b = re.findall(r'<lang n="greek">.*?</lang>',line)
  for x in b:
   a.append(x)
 return a

class Data:
 def __init__(self,metaline,ngreek,ngreekab):
  self.metaline = metaline
  self.ngreek = ngreek # csl
  self.ngreekab = ngreekab  #Ab version
  
def check_greek(entries,entriesab):
 nprob = 0
 ngreek = 0
 ngreekab = 0
 datarr = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  greeks = greek_instances(entry)
  greeksab = greek_instances(entryab)
  if (greeks == []) and (greeksab == []):
   continue
  if len(greeksab) != 0:
   ngreekab = ngreekab + 1
  if len(greeks) != 0:
   ngreek = ngreek + 1
  if len(greeks) != len(greeksab):
   nprob = nprob + 1
  data = Data(entry.metaline,len(greeks),len(greeksab))
  datarr.append(data)
 print(ngreek,'entries with Greek phrases in csl')
 print(ngreekab,'entries with Greek phrases in ab')
 print(nprob,'entries with different number of greek phrases')
 return datarr

def write_datarr(fileout,a):
 outarr = []
 ndiff = 0
 for data in a:
  meta = re.sub(r'<k2>.*$','',data.metaline)
  n = data.ngreek
  nab = data.ngreekab
  if n == nab:
   flag = '=='
  else:
   flag = '!='
   ndiff = ndiff+1
  out = '%s %s %s %s' %(n,flag,nab,meta)
  outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for iline,line in enumerate(outarr):
   f.write(line+'\n')
 print(len(outarr),"records written to",fileout)
 print(ndiff,"entries with differences to resolve")

if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileab = sys.argv[2] # bop ab
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict
 digentry.Entry.Ldict = {}
 entriesab = digentry.init(fileab)
 Ldictab = digentry.Entry.Ldict

 check_entries_L(Ldict,Ldictab)
 
 check_metaline(entries,entriesab)
 datarr = check_greek(entries,entriesab)
 write_datarr(fileout,datarr)

 

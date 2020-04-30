#-*- coding:utf-8 -*-
"""preverb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

class SLP1(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  m = re.search(r'^<e>.*<in>(.*?)</in> <out>(.*?)</out>',line)
  if not m:
   self.status = False
   #print('SLP1 skip:',line)
   return
  self.status = True
  self.slp1 = m.group(1)
  self.romanraw = m.group(2)
  self.roman = transcoder.transcoder_processString(self.slp1,"slp1","roman")

def init_slp1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = []
  for line in f:
   rec = SLP1(line)
   if rec.status:
    recs.append(rec)
 return recs

def write(fileout,recs):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0
  a = [] # lower case letters in rec.roman
  b = [] # upper case
  for rec in recs:
   if len(rec.slp1) == 1:
    n = n + 1
    rup = rec.roman.upper()
    f.write('%s %s %s\n' %(rec.slp1,rec.roman,rup))
    for x in rec.roman:
     if x not in a:
      a.append(x)
    for x in rup:
     if x not in b:
      b.append(x)
  a.sort()
  b.sort()
  astr = ''.join(a)
  bstr = ''.join(b)
  f.write('lowerslp=%s\n'%astr)
  f.write('upperslp=%s\n'%bstr)
 print(n,"records written to",fileout)
 #print(a)
 #print(b)

if __name__=="__main__": 
 filein = sys.argv[1]  # slp1_roman.xml
 fileout = sys.argv[2] # 
 recs = init_slp1(filein)
 write(fileout,recs)

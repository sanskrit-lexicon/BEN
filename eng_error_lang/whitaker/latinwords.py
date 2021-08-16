# This Python file uses the following encoding: utf-8
"""latinwords.py
  extract wordlist from DICTPAGE.RAW
  non-unicode UTF-8 characters changed in place.
  Also use Emacs revert-buffer-with-encoding utf-8
 line 6851  non-unicode bovid[e-acute].    Change to unicode é
 Same with line 37398.

"""
from __future__ import print_function
import sys,codecs,re

class Latin(object):
 def __init__(self,line):
  self.line = line.rstrip('\r\n')
  self.head = None
  self.use = True
  #print(self.line)
  
def simplify(rec):
 x = rec.line
 x1 = re.sub(r' +\[.....\].*$','',x) # remove gloss and ending spaces
 x2 = re.sub(r' +',' ',x1)
 rec.head = x2
 if ' abb.' in rec.head:
  rec.use = False
 # remove initial '#'
 x3 = re.sub(r'^#','',x2)
 # remove parts of speech
 x4 = re.sub(r' [MFN]\b','',x3)
 x5 = re.sub(r' (ABL|ACC|ADJ|ADV|V|INTRANS|TRANS|PREP|INTERJ|DEP|SEMIDEP|C|sum|NUM||PRON|REFLEX)\b','',x4)
 x6 = re.sub(r' (([(]2nd[)])|([(]1st[)])|([(]3rd[)])|([(]4th[)])|([(]5th[)]))','',x5) # why doesn't work?
 x7 = x6.replace(' -',' ')
 x8 = x7.replace(' (gen.)',' ')
 x9 = re.sub(r'\(ii?\)','',x8)
 #x9 = x8.replace('(ii)','')
 x10 = re.sub(r' \(gen ','(',x9)
 x11 = re.sub(r' \(GEN\)',' ',x10)
 rec.head = x11
 
def init_latin(filein):
 with codecs.open(filein,"r",'utf-8') as f:
  recs = [Latin(x) for x in f if not x.startswith(';')]
 print(len(recs),"records from",filein)
 return recs

def write_lines(recs,fileout):
 with codecs.open(fileout,"w",'utf-8') as f:
  n = 0
  nskip = 0
  nword = 0
  nblank = 0
  #allwords = []
  d = {}
  for rec in recs:
   if not rec.use:
    continue
   words = rec.head.split(',')
   for word in words:
    word = word.strip() # remove space at ends
    if word == '':
     nblank = nblank + 1
     continue
    if word in d:
     continue
    d[word] = True
    m = re.search(r'[^a-z]',word)
    if m:
     f.write(';?%s\n'%word)
     nskip = nskip + 1
    else:
     f.write(word+'\n')
     nword = nword + 1
   n = n + 1
 print(nword,"words written to",fileout)
 print(nskip,";? non-words also written")
 print(nblank,"blank words skipped")
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 recs = init_latin(filein)
 for rec in recs:
  simplify(rec)
 write_lines(recs,fileout)
 

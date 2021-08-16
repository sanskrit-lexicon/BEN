# This Python file uses the following encoding: utf-8
"""mark_lang.py
   
"""
from __future__ import print_function
import sys,codecs,re

class Suggest(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  self.L,self.k1,self.word = line.split(':')
  self.latin = False
  
def init_suggestions(filein):
 with codecs.open(filein,"r",'utf-8') as f:
  words = [Suggest(x) for x in f if not x.startswith(';')]
 print(len(words),"correction suggestions read from",filein)
 return words

def mark_latin(recs,dlatin):
 n = 0
 for rec in recs:
  rec.latin = rec.word in dlatin
  if rec.latin:
   n = n + 1
 print(n,"suggestion words are Latin")
 
def init_latin(filein):
 with codecs.open(filein,"r",'utf-8') as f:
  words = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 print(len(words),"Latin words from",filein)
 return words

def writeok(recs,fileout,langcode):
 with codecs.open(fileout,"w",'utf-8') as f:
  n  = 0
  for rec in recs:
   line = rec.line
   if rec.latin:
    n = n + 1
    out = '%s:OK:%s' % (line,langcode)
    f.write(out + '\n')
 print(n,"records written to",fileout)

def writetodo(recs,fileout):
 with codecs.open(fileout,"w",'utf-8') as f:
  n = 0
  for rec in recs:
   line = rec.line
   if not rec.latin:
    f.write(line + '\n')
    n = n + 1
 print(n,"records written to",fileout)

if __name__=="__main__":
 langcode =  sys.argv[1]
 filein = sys.argv[2]
 filelatin = sys.argv[3]
 fileok = sys.argv[4]
 filetodo = sys.argv[5]
 latinwords = init_latin(filelatin)
 dlatin = {}
 for x in latinwords:
  dlatin[x] = True
 recs = init_suggestions(filein)
 mark_latin(recs,dlatin)
 writeok(recs,fileok,langcode)
 writetodo(recs,filetodo)

#-*- coding:utf-8 -*-
"""change1.py 
 
"""
import sys,re,codecs
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 
class Change(object):
 def __init__(self,metaline,page,iline,old,new,reason,iline1,line1,new1):
  self.metaline = metaline
  self.page = page
  self.iline = iline
  self.old = old
  self.new = new
  self.reason = reason
  self.iline1 = iline1
  self.line1 = line1
  self.new1 = new1
def change1(line):
 reason = 'marked'
 if '</ls>' not in line:
  return reason,line
 newline = re.sub(r'</ls>(-[0-9]+)',r'\1</ls>',line)
 newline = re.sub(r'</ls>-(-[0-9]+)',r'\1</ls>',newline)
 return reason,newline

def change_out(change,ichange):
 outarr = []
 case = ichange + 1
 #outarr.append('; TODO Case %s: (reason = %s)' % (case,change.reason))
 try:
  ident = '%s  (reason = %s)' %(change.metaline,change.reason)
 except:
  print('ERROR:',change.iline,change.old)
  exit(1)
 if ident == None:
  ident = change.page
 outarr.append('; ' + ident)
 # change for iline
 lnum = change.iline + 1
 line = change.old
 new = change.new
 outarr.append('%s old %s' % (lnum,line))
 outarr.append('%s new %s' % (lnum,new))
 outarr.append(';')
 #change for iline1
 if True:
  lnum = change.iline1 + 1
  line = change.line1
  new = change.new1
  outarr.append('%s old %s' % (lnum,line))
  outarr.append('%s new %s' % (lnum,new))
  outarr.append(';')

 # dummy next line
 return outarr

def change_out_simple(change,ichange):
 outarr = []
 # change for iline
 lnum = change.iline + 1
 line = change.old
 new = change.new
 if change.metaline == None:
  outarr.append('; not entry')
 outarr.append('%s old %s' % (lnum,line))
 outarr.append(';')
 outarr.append('%s new %s' % (lnum,new))
 outarr.append('; ----')

 # dummy next line
 return outarr

def write_changes(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
   for ichange,change in enumerate(changes):
    outarr = change_out_simple(change,ichange)
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"change transactions written to",fileout)

def suspectwords(line):
 parts = re.split(r'({%.*?%})|(<ls>.*?</ls>)|(<ab>.*?</ab>)|(<.*?>)',line)
 newparts = []
 words = []
 for part in parts:
  if part == None:
   pass
  elif part.startswith('{%'):
   newpart = part
  elif part.startswith('<'):
   newpart = part
  elif not re.search(r'[Ṣṣ]',part):
   newpart = part
  else:
   a = re.split(r'\b',part) 
   for x in a:
    if re.search(r'[Ṣṣ]',x):
     words.append(x)
 return words

def init_shwords(lines):
 changes = [] # array of Change objects
 metaline = None
 shwords = {}
 for iline,line in enumerate(lines):
  words = suspectwords(line)
  for word in words:
   if word not in shwords:
    shwords[word] = 0
   shwords[word] = shwords[word] + 1
 return shwords


def write_shwords(fileout,shwords):
 words = sorted(shwords.keys())
 with codecs.open(fileout,"w","utf-8") as f:
   for word in words:
    out='%s %s'%(word,shwords[word])
    outarr = [out]
    for out in outarr:
     f.write(out+'\n')
 print(len(words),"Ṣṣ words written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # possible change transactions
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 shwords = init_shwords(lines)
 write_shwords(fileout,shwords)

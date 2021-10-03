#-*- coding:utf-8 -*-
"""changepc.py 
 
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
 #if change.metaline == None:
 # outarr.append('; not entry')
 outarr.append('%s old %s' % (lnum,line))
 #outarr.append(';')
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

def suspectwords(line,shwords):
 parts = re.split(r'({%.*?%})|(<ls>.*?</ls>)|(<ab>.*?</ab>)|(<.*?>)',line)
 newparts = []
 words = []
 for part in parts:
  if part == None:
   continue
  elif part.startswith('{%'):
   newpart = part
  elif part.startswith('<'):
   newpart = part
  elif not re.search(r'[Ṣṣ]',part):
   newpart = part
  else:
   a = re.split(r'\b',part)
   b = []
   for x in a:
    if x in shwords:
     y = x.replace('ṣ','sh')
     y = y.replace('Ṣ','Sh')
     # also update found count in shwords
     shwords[x][1] = shwords[x][1] + 1
    else:
     y = x
    b.append(y)
   newpart = ''.join(b)
  newparts.append(newpart)
 newline = ''.join(newparts)
 return newline

def init_changes(lines,shwords):
 changes = [] # array of Change objects
 metaline = None
 for iline,line in enumerate(lines):
  newline = suspectwords(line,shwords)
  if newline == line:
   continue
  # insert the hyphen in next line
  iline1 = None #iline + 1
  line1 = None # lines[iline1]
  newline1 = None
  reason = None
  page = None
  change = Change(metaline,page,iline,line,newline,reason,iline1,line1,newline1)  
  changes.append(change)
 return changes

def write_changes(fileout,pcerrs):
 outrecs = []
 for pcerr in pcerrs:
  outarr = []
  oldpc = pcerr.oldpc
  newpc = pcerr.newpc
  pclines = pcerr.lines
  outarr.append('; -----------------------------------------------------')
  outarr.append('; %s -> %s (%s changes)' %(oldpc,newpc,len(pclines)))
  for pcline in pclines:
   lnum,metaline = pcline.split(':')
   newline = metaline.replace(oldpc,newpc)
   assert newline != metaline
   outarr.append('%s old %s' %(lnum,metaline))
   outarr.append('%s new %s' %(lnum,newline))
   outarr.append(';')
  outrecs.append(outarr)

 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print("changes written to",fileout)

class PCerr(object):
 def __init__(self,oldpc,newpc):
  self.oldpc = oldpc
  self.newpc = newpc
  self.lines = []
 def append(self,line):
  assert '<L>' in line
  pc = '<pc>' + self.oldpc
  if pc not in line:
   print('ERROR',pc,'line=',line)
   exit(1)
  #assert pc in line
  self.lines.append(line)
  
def generate_pcerrs(lines):
 for iline,line in enumerate(lines):
  if line.startswith(';'):
   m = re.search(r'^; ([0-9][0-9][0-9][0-9]-[ab]) -> ([0-9][0-9][0-9][0-9]-[ab])',line)
   assert m != None
   oldpc = m.group(1)
   newpc = m.group(2)
   if iline != 0:
    yield pcerr
   pcerr = PCerr(oldpc,newpc)   
  else:
   pcerr.append(line)
 # yield last group
 yield pcerr
 
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # list of words to change
 fileout = sys.argv[3] # possible change transactions
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 with codecs.open(filein1,"r","utf-8") as f:
  pcerrlines = [line.rstrip('\r\n') for line  in f]
 pcerrs = list(generate_pcerrs(pcerrlines))
 print(len(pcerrs),"pc groups found")
 nc = sum(len(pcerr.lines) for pcerr in pcerrs)
 print('nc=',nc)
 write_changes(fileout,pcerrs)

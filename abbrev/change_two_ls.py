#-*- coding:utf-8 -*-
"""change_two_ls.py for Benfey abbreviations
 
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

def write_changes(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
   for ichange,change in enumerate(changes):
    outarr = change_out(change,ichange)
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"possible changes written to",fileout)

def write_changes_hyphen(fileout,changes):
 # aggregate via reason
 aggs = {}
 for change in changes:
  reason = change.reason
  if reason not in aggs:
   aggs[reason] = []
  aggs[reason].append(change)
 
 with codecs.open(fileout,"w","utf-8") as f:
  reasons = aggs.keys()
  nchanges = 0
  for reason in reasons:
   changes1 = aggs[reason]
   f.write('; --------------------------------------------------------------\n')
   f.write(';  hyphen = %s, %s instances\n' %(reason,len(changes1)))
   f.write('; --------------------------------------------------------------\n')
   for ichange,change in enumerate(changes1):
    outarr = change_out(change,ichange)
    for out in outarr:
     f.write(out+'\n')
   nchanges = nchanges + len(changes1)
 print(nchanges,"possible changes written to",fileout)

class Tooltip(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = re.split(r' += ',line)
  if len(parts) != 2:
   print('problem parsing tooltip')
   print(line)
   print(parts)
   exit(1)
  self.abbrev,self.tip = parts
  self.nabbrev = 0
  self.awords = re.split(r' +',self.abbrev)
  
def init_tooltip(filein):
 with codecs.open(filein,"r","utf-8") as f:
  ans = []
  for x in f:
   tip = Tooltip(x)
   if len(tip.awords) != 1:
    #print(tip.abbrev)
    ans.append(tip)
 print(len(ans),'tooltips from',filein)
 return ans

def preparetips1(s):
 words = s.split(' ')
 ans = []
 nw = len(words)
 # split words into two non-empty parts
 if len(words) == 2:
  ans = [words]
 elif len(words) == 3:
  ans = [
    [' '.join(words[0:1]),' '.join(words[1:nw])],
    [' '.join(words[0:2]),' '.join(words[2:nw])]
  ]
 else:
  print('ERROR: preparetips_test. Cannot handle %s words',s)
  exit(1)
 #print(ans)
 return ans
def preparetips(tips):
 recs = []
 for tip in tips:
  tip.segments = preparetips1(tip.abbrev)
  for segment in tip.segments:
   recs.append(segment)  # a two-tuple (a,b)
 # sort segments in decreasing order of length of 'a'
 #tooltips = sorted(tooltips1,key = lambda tip: len(tip.abbrev),reverse=True)
 recs = sorted(recs,key = lambda rec: len(rec[0]),reverse = True)
 return recs
def init_changes(lines,tips):
 segments = preparetips(tips)  # compute segments attribute for each tip
 changes = [] # array of Change objects
 metaline = None
 nabbrev = 0  # number of abbreviations marked
 nlines = len(lines)
 print('nlines=',nlines)
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   continue
  if line.startswith('<LEND>'):
   metaline = None
   continue
  if line.startswith('<H>ADDENDA'):
   # ADDENDA AND CORRIGENDA
   metaline = 'ADDENDA'
   continue
  if line.startswith('[Page'):
   page = line
   continue
  if metaline == None:
   continue
  found = False
  iline1 = iline + 1
  if iline1 < nlines:
   line1 = lines[iline1]
  else:
   # last line. cannot match
   continue
  for (a,b) in segments:
   if not re.search(r'%s *$'%a,line):
    continue
   if not re.search(r'%s%s'%('<div n="lb">',b),line1):
    if a not in ['Lass.','Kāvya','Böhtl.']:
     print('manual check needed')
     print('%s old %s' %(iline+1,line))           
     print('%s old %s' %(iline1+1,line1))
    continue
   found = True
   break
  if not found:
   continue
  # generate a Change instance
  # remove hyphen phrase in line
  newline = re.sub(r'%s *$'%a,'',line)  
  # insert 'a' into next line
  #iline1 = iline + 1
  #line1 = lines[iline1]
  #print('hyphen=',hyphen)
  old = '<div n="lb">'
  new = '%s%s ' %(old,a)
  newline1 = line1.replace(old,new)
  if newline1 == line1:
   # unexpected next line
   # add note to metaline
   metaline = metaline + '  PROBLEM'
  reason = '%s LB %s' %(a,b)
  change = Change(metaline,page,iline,line,newline,reason,iline1,line1,newline1)  
  changes.append(change)
  # reset next line in case it also requires a change
  lines[iline1] = newline1
 return changes

def test():
 trials = ['x y','x y z']
 for trial in trials:
  ans = preparetips_test(trial)
  print('%s => %s' %(trial,ans))
  
if __name__=="__main__":
 #test()
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filetip = sys.argv[2]
 fileout = sys.argv[3] # possible change transactions
 tips = init_tooltip(filetip) # tooltips with 2 or more words in abbreviation

 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # lines = lines  # for later comparison
 changes = init_changes(lines,tips)
 # cannot aggregate by 'reason', as order is sometimes important,
 # namely when two successive lines change
 #write_changes_hyphen(fileout,changes)
 write_changes(fileout,changes)

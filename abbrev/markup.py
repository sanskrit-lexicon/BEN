#-*- coding:utf-8 -*-
"""markup.py for Benfey abbreviations
 
"""
import sys,re,codecs
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 


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
  # abbrevalt.  If tip starts with lower-case, abbrevalt upcases 1st letter.
  # otherwise abbrevalt is None
  # Used to generate warning messages
  a = self.abbrev.capitalize() # upcase 1st letter
  if a != self.abbrev:
   self.abbrevalt = a
  else:
   self.abbrevalt = None
  self.tipaltFound = False  # set to true if abbrevalt is in the list of 

def init_tipaltFound(tips):
 # dictionary of tip abbrevs
 d = {}
 for tip in tips:
  d[tip.abbrev] = True
 #
 n = 0
 for tip in tips:
  if tip.abbrevalt in d:
   tip.tipaltFound = True
   #print('chk:',tip.abbrev,tip.abbrevalt)
   n = n + 1
 print("init_tipaltFound",n)
 
def init_tooltip(filein):
 with codecs.open(filein,"r","utf-8") as f:
  ans = [Tooltip(x) for x in f]
 print(len(ans),'tooltips from',filein)
 init_tipaltFound(ans)
 return ans

def mark(tip,oldlines,tag):
 abbrev = tip.abbrev
 abbrevreg = abbrev.replace('.','[.]')
 abbrev_marked = '<%s>%s</%s>' % (tag,abbrev,tag)
 abbrevcap = abbrev.capitalize()
 tipaltFound = tip.tipaltFound
 notcap = (abbrev != abbrevcap)  # flag: abbrev already capitalized
 #print('notcap=',notcap,abbrevcap)
 ncap = 0
 dbgcap = True
 newlines = []
 metaline = None
 exclude_chars = r'[a-zA-Z0-9ÆÑÖàáäæéêëíïñóôöúüÿĀāăēĕĪīĭōŏœŚśŪūŭ̆ḌḍḤḥḶḷṂṃṄṅṆṇṚṛṜṝṢṣṬṭạ]'
 nabbrev = 0  # number of abbreviations marked
 for iline,line in enumerate(oldlines):
  if line.startswith('<L>'):
   metaline = line
   newlines.append(line)
   continue
  if line.startswith('<LEND>'):
   metaline = None
   newlines.append(line)
   continue
  if line.startswith('<H>ADDENDA'):
   # ADDENDA AND CORRIGENDA
   metaline = True
   newlines.append(line)
   continue
  if metaline == None:
   newlines.append(line)
   continue
  if not (abbrev in line):
   # do this first for efficiency
   newlines.append(line)
   if dbgcap:  # for prelim debugging
    if notcap:
     # check if capitalization present
     if abbrevcap in line:
      ncap = ncap + 1
   continue
  # split on xml tags
  #parts = re.split(r'(<.*?>)|(<.*?</.*?>)',line)
  #parts = re.split(r'(<.*?>)|(<.*?</.*?>)',line)
  #parts = re.split(r'(<.*?</.*?>)|(<.*?>)',line)
  parts = re.split(r'(<div n="lb">)|(<ab>.*?</ab>)|(<ls>.*?</ls>)|(<lang n="greek"></lang>)|(<HI>)|(<P>)',line)
  if True and ((iline+1) in [10395]) and (tag == 'ls'): print(iline+1,line,"\n",parts)
  newparts = []
  for part in parts:
   if part == None:
    continue
   if part.startswith('<'):
    newpart = part
   else:
    if re.search(r'%s%s'%(exclude_chars,abbrevreg),part):
     # skip false positive.  example 'd.' (distich) can be end of word ('send.')
     newpart = part
    else:
     newpart = part.replace(abbrev,abbrev_marked)
     if newpart != part:
      nabbrev = nabbrev+1
      #if (iline == 2786) and (tag == 'ab'):
      # print('dbg: part=%s  AND newpart=%s' %(part,newpart))
   newparts.append(newpart)
  newline = ''.join(newparts)
  newlines.append(newline)
  if False and (newline != line):
   print('%s old %s' %(iline+1,line))
   #print('%s new %s' %(iline+1,newline))
 tip.nabbrev = nabbrev
 if ncap > 0:
  if not tipaltFound:
   print('WARNING: MISSED %s instances of capitalized'%ncap,abbrevcap,tipaltFound)
 return newlines

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 tag = sys.argv[2]  # ls or ab
 filetip = sys.argv[3] # Tooltip file
 fileout = sys.argv[4] # revised xxx.txt
 filestat = sys.argv[5]  # count of abbreviations in filetip that are marked
 n = 0
 tips0 = init_tooltip(filetip)
 # sort tips so longest tooltip abbreviation comes first
 tips = sorted(tips0,key = lambda tip: len(tip.abbrev),reverse=True)
 # read digitization as lines
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 fstat = codecs.open
 oldlines = lines
 for tip in tips:
  newlines = mark(tip,oldlines,tag)
  oldlines = newlines
  #print('breaking early')
  #break
 with codecs.open(fileout,"w","utf-8") as f:
  for iline,line in enumerate(newlines):
   f.write(line+'\n')
 with codecs.open(filestat,"w","utf-8") as f:
  ntot = 0
  for tip in tips0:  # in same order as ben_ls
   if tag == 'ab':
    ab = tip.abbrev.ljust(10)
   else:
    ab = tip.abbrev.ljust(15)
   f.write('%04d %s = %s\n' % (tip.nabbrev,ab,tip.tip[0:50]))
   ntot = ntot + tip.nabbrev
  f.write('%d All <%s> tags\n' %(ntot,tag))
 print('statistics written to',filestat)

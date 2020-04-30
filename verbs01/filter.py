#-*- coding:utf-8 -*-
"""filter.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#from ccs_verb_filter_map import init_mwverbs
#import transcoder
#transcoder.transcoder_set_dir('transcoder')
from ccs_verb_filter_map import init_caeverb

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None
  self.nasal = None

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

# next 3 from hwnorm1/sanhw1/hwnorm1c.py
slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}

def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)

def homorganic_nasal(a):
 return re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)

def map2mw_nasal(k1,d):
 k = homorganic_nasal(k1)
 print('map2mw_nasal: %s -> %s (%s)'%(k1,k,k in d))
 if k in d:
  return k
 return None

def insert_nasal(k1,d):
 c = k1[-1]
 if c not in slp1_cmp1_helper_data:
  return None
 nasal = slp1_cmp1_helper_data[c]
 k = k1[0:-1] + nasal + c
 ans = map2mw_nasal(k,d)
 return ans

def lexflag(line):
 lexpatterns = [
   '¦.*?{%m[.]',  #masculine
   '¦.*?{%f[.]',  #feminine
   '¦.*?{%n[.]',  #neuter
   '¦.*?{%adv[.]',  #adverb
   '¦.*?{%s[.]',  #see
  """
   '¦.*? <ab>a.</ab>',  #adjective
   '¦.*? <ab>ind.</ab>',  # indeclineable
   '¦.*? interj[.]',  # interjection
   '¦.*? <ab>adv.</ab>',  # adverb
   """
 ] 
 for pattern in lexpatterns:
  m = re.search (pattern,line)
  if m:
   return True
 return False

def mark_entries(entries):
 n = 0
 for entry in entries:
  # first exclude known non-verbs
  L  = entry.metad['L']
  k1 = entry.metad['k1']
  k2 = entry.metad['k2']
  if lexflag(entry.datalines[0]):  # exclude adverbs, etc.
   continue
  m = re.search(r'¦.*t[ie]#}',entry.datalines[0])
  if not m:
   continue
  entry.markcode = True
  n = n + 1
 print(n,"entries marked as verb")

def init_caed(caerecs):
 d = {}
 for rec in caerecs:
  k1 = rec.k1
  if k1 not in d:
   d[k1] = []
  d[k1].append(rec)
 return d

def write_lines(fileout,entries,caerecs):
 caed = init_caed(caerecs)
 n = 0
 ncae = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   k1 = entry.metad['k1']
   #print(" '%s':'',  # " %k1)
   if k1 in caed:
    x = ' (in cae)'
    ncae = ncae + 1
    continue
   else:
    x = ' (not cae)'
   n = n + 1
   outarr = ['* ' +entry.metaline+x]
   lines = entry.datalines
   for line in lines:
    outarr.append('; ' + line) 
   outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
 print('%04d' %n,"records written to",fileout)
 print(ncae,"ccs verbs are in cae")

def init_Lnums(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = []
  for line in f:
   line = line.rstrip()
   m = re.search(r'L=(.*?),',line)
   if m:
    recs.append(m.group(1))
 print(len(recs),"records read from",filein)
 return recs

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # cae_verb_filter.txt
 fileout = sys.argv[3] # 
 entries = init_entries(filein)
 mark_entries(entries)
 caerecs = init_caeverb(filein1)

 write_lines(fileout,entries,caerecs)

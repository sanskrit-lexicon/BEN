#-*- coding:utf-8 -*-
"""changes_1.py accent work
 
"""
import sys,re,codecs

def parseheadline(headline):
 """<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1<e>2"""
 headline = headline.strip()
 splits = re.split('[<]([^>]*)[>]([^<]*)',headline)
        #print(splits)
 result = {}
 for i in range(len(splits)):
  if i % 3 == 1:
   result[splits[i]] = splits[i+1]
 return result

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
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
  self.langlines = []
  self.langflag = False
  
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

def notify_out(metaline,lnum,line):
 outarr = []
 outarr.append('; %s'%metaline)
 outarr.append('%s old %s' %(lnum,line))
 outarr.append(';')
 return outarr

def change_out(metaline,lnum,line,new):
 outarr = []
 outarr.append('; %s'%metaline)
 outarr.append('%s old %s' %(lnum,line))
 outarr.append('%s new %s' %(lnum,new))
 outarr.append(';')
 return outarr

def change_out_phrase(metaline,lnum,line,new,phrase):
 outarr = []
 outarr.append('; %s'%metaline)
 outarr.append('; x = %s' %phrase)
 outarr.append('%s old %s' %(lnum,line))
 outarr.append('%s new %s' %(lnum,new))
 outarr.append(';')
 return outarr

def change_out_prev(metaline,lnum,line,new,lnumprev,lineprev):
 outarr = []
 outarr.append('; %s'%metaline)
 outarr.append('%s old %s' %(lnumprev,lineprev))
 outarr.append('%s new %s' %(lnumprev,lineprev))
 outarr.append(';')
 outarr.append('%s old %s' %(lnum,line))
 outarr.append('%s new %s' %(lnum,new))
 outarr.append(';')
 outarr.append(';')
 return outarr

def mark_entry(entry,langcode):
 # remove markup
 lines = [re.sub(r'<.*?>','',line) for line in entry.datalines]
 keeplines = []
 langreg = langcode.replace('.','[.]')
 flag = False
 for iline,line in enumerate(lines):
  if langcode in line:
   line1 = re.sub(r'^.*%s' %langreg,langcode,line)
   #keeplines.append(line1)
   # also, next line, if it exists
   try:
    line2 = lines[iline+1]
    lineout = line1 + ' ' + line2
   except:
    lineout = line1
   # simplify in a few ways
   
   lineout = re.sub(r'^%s ([a-z]+)[;.](.*)$'%langreg,
                    r'%s = \1'%langcode,lineout)
   keeplines.append(lineout)
 entry.langlines = keeplines
 entry.langflag = (len(entry.langlines) != 0)
 
def out1(entry):
 outarr = []
 if not entry.langflag:
  return outarr
 outarr.append(entry.metaline)
 outarr = outarr + entry.langlines
 return outarr

def write(fileout,entries,langcode):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0 # number of entries with langcode
  for entry in entries:
   outarr = out1(entry)
   n = n + len(outarr)
   for out in outarr:
    f.write(out+'\n')
 print(n,"entries with language code",langcode,"written to",fileout)
 
if __name__=="__main__":
 langcode = sys.argv[1]
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[3] # possible change transactions
 regexraw1 = r'{#[^#]*?([a-zA-Z0-9\^\\]+[~][\^\\/]+[a-zA-Z0-9]*)'  

 print(regexraw1)
 regex1 = re.compile(regexraw1)

 entries = init_entries(filein)
 for entry in entries:
  mark_entry(entry,langcode)
 write(fileout,entries,langcode)

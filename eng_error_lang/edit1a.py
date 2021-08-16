from __future__ import print_function
import sys,codecs,re

def parse(lines,langcode):
 langreg = langcode.replace('.','[.]')
 a = []
 for line in lines:
  if line.startswith('<L>'):
   a.append(line)
   continue
  m = re.search(r'^(%s)(.*)$'%langreg,line)
  x = m.group(2)
  x = re.sub(r'[,;.]',' ',x)
  x = x.strip()
  words = re.split(r' +',x)
  for word in words:
   a.append('%s %s'%(langcode,word))
 return a
if __name__=="__main__":
 langcode = sys.argv[1]
 filein = sys.argv[2]
 fileout = sys.argv[3]
 with codecs.open(filein,"r",'utf-8') as f:
  lines = [x.rstrip('\r\n') for x in f]
 langreg = langcode.replace('.','[.]')
 d = {}
 words = []
 for line in lines:
  m = re.search(r'%s (.*)$' %langreg,line)
  if not m:
   continue
  w = m.group(1)
  if w not in d:
   d[w] = True
   words.append(w)
   
 words = sorted(words)
 with codecs.open(fileout,"w","utf-8") as f:
  for word in words:
   f.write(word+'\n')
 print(len(words),"words written to",fileout)
 
   

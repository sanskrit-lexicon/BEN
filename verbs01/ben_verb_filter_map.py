#-*- coding:utf-8 -*-
"""ccs_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Ccsverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  try:
   self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  except:
   print('Ccsverb error:',line)
   exit(1)
  self.pw=None
  self.mw = None
 
def init_ccsverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Ccsverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Pwmw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.pw,self.mw = line.split(':')
 
def init_pw_mw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Pwmw(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

map2mw_special = {
 'ucC':'uC',
 'utkaRW':'utkaRWa',  #
 #'ulaRq':'ulaRq',  #
 'U':'u',  #
 'Un':'Unaya',  #
 #'fkz':'fkz',  #
 'kadarT':'kadarTaya',  #
 'kamalAhAs':'kamalAhAsa',  #
 'karakAsAr':'karakAsAra',  #
 'karpUr':'karpUra',  #
 'kAl':'kAlaya',  #
 'kuwumb':'kuwumbaya',  #
 'kumAr':'kumAraya',  #
 'kumAl':'kumAlaya',  #
 'kusm':'kusmaya',  #
 #'kfRv':'kfRv',  #
 'ket':'ketaya',  #
 #'kraSaya':'kraSaya',  #
 #'kzAraya':'kzAraya',  #
 #'kzIraya':'kzIraya',  #
 'garD':'gfD',  #
 'gAtr':'gAtraya',  #
 #'giraya':'giraya',  #
 'guR':'guRaya',  #
 'gfh':'grah',  #
 'gom':'gomaya',  #
 'gozw':'gozwa',  #
 'grAm':'grAmaya',  #
 'GuMz':'GaMz',  #
 'citr':'citraya',  #
 'Card':'Cfd',
 #'Calaya':'Calaya',  #
 'Cidr':'Cidraya',  #
 'jurv':'jUrv',  #
 'jfB':'jfmB',  #
 #'jyAya':'jyAya',  #
 'tantr':'tantraya',  #
 'taraNg':'taraMgaya',  # or? taraMga
 #'tirohaya':'tirohaya',  #
 'tIr':'tIraya',  #
 'tutT':'tutTaya',  #
 'tUr':'tur',  #
 'tfMh':'tfh',  #
 'tfn':'tfR',  #
 'trA':'trE',
 'daRq':'daRqaya',  #
 'daridrA':'drA', # desiderative
 'duHK':'duHKaya',  #
 'drAGaya':'drAG',  # 
 'palpUl':'palpUlaya',  #
 'pAr':'pAraya',  #
 'pIyUz':'pIyUza',  #
 'pIv':'pIva',  #
 'puzp':'puzpAya',  # ?
 'pUr':'pF',  #
 'pUrb':'purv',  #
 'pUrv':'purv',  #
 'pfYc':'pfc',  #
 'prakaw':'prakawa',  #
 'preNKol':'preNKola',  #
 'baw':'vaw',  #
 'ban':'van',  #
 'baz':'vaz',  #
 'bas':'vas',  #
 'bIBatsa':'bAD',  # 'anomalous desiderative'
 'BAj':'Baj',  #
 'mImAMsa':'man',  # desidr.
 'mUtr':'mUtraya',  #
 'mfYj':'muj',  #
 'lambaya':'lamb',  #
 'var':'vf',  #
 'varz':'parz',  #
 #'vAzpAya':'vAzpAya',  #
 'vfc':'vfj',  #
 'vfYj':'vfj',  #
 'vraYj':'vraj',  #
 'vrUz':'vrUs',  #
 'SaMst':'sas',  # ?
 'zwamB':'stamB',  #
 'zwyE':'styE',  #
 'zvask':'svask',  #
 'saMket':'saMketaya',  #
 'sAr':'SAr',  #
 'sraMS':'sraMs',  #
 #'sval':'sval',  #
 'svurC':'sPurC',  #
 'haMs':'haMsa',  #
 'hAr':'hAra',  #

  # to accomodate preverb matching
 'kurd':'kUrd',
 'kzaR':'kzan',
 'DUp':'DUpaya',
 'und':'ud',
 'fc':'arc',
}


map2mw_special_L = {
 #'19122':'san', # sA
 #'19123':'so', # sA
}


def map2mw(d,k1,L):
 if L in map2mw_special_L:
  k =  map2mw_special_L[L]
  if k in d:
   return k
  else:
   print('map2mw anomaly 1',L,k1,k)
 if k1 in map2mw_special:
  k = map2mw_special[k1]
  if k in d:
   return k
  else:
   print('map2mw anomaly 1',L,k1,k)
 if k1 in d:
  return k1

 if k1.endswith('y'):
  k = k1 + 'a'
  if k in d:
   return k
 
 return '?'


def ccsmap(recs,mwd):
 for rec in recs:
  rec.mw = map2mw(mwd,rec.k1,rec.L)
  #if rec.k1 in ['aNkay','aNKay']:print('ccsmap chk: %s -> %s (%s)' %(rec.k1,rec.mw,rec.mw in mwd))
def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw
   out = '%s, mw=%s' %(line,rec.mw)
   if rec.mw == '?':
    nomw = nomw + 1
   f.write(out + '\n')
 print(n,"records written to",fileout)
 print(nomw,"records not yet mapped to mw")


if __name__=="__main__": 
 filein = sys.argv[1] #  ccs_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_ccsverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 ccsmap(recs,mwverbsd)
 write(fileout,recs)


Analysis of ben verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs) of csl-orig/v02/ben/.

The shell script redo.sh reruns 5 python programs, from mwverb.py to preverb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* prepare roman
python roman.py transcoder/slp1_roman.xml roman.txt
This gets a starting list of upper-case IAST letters used in transliteration
of verbs
* ben_verb_filter.

python ben_verb_filter.py ../ben.txt   ben_verb_exclude.txt ben_verb_filter.txt

Verbs entries in BEN are recognized by having an upper-case transliteration
following the Devanagari headword.
In terms of the Cologne digitization, this is found by the pattern:
V: u'¦ *{%[ABCDGHIJKPTUÑĀĪŚŪ̃ḌḤḶḸṂṄṆṚṜṢṬSNMRVLYEO‡,.;:-]+%}',
W: u'¦ {%[^%]*[A-Z]'
   Example: {#† glas#}¦ {%GLAS = gras.%}


2050 entries are thus identified as verbs, out of 17313 entries (9.9%).

The exclusion file is empty for BEN (no false positives to exclude thus far).

Format of file ben_verb_filter.txt:
;; Case 0001: L=2, k1=aMS, k2=aMS, code=V


* ben_verb_filter_map
python ben_verb_filter_map.py ben_verb_filter.txt mwverbs1.txt ben_verb_filter_map.txt

Get correspondences between ben verb spellings and
 - ben verb spellings
 - mw verb spellings

Format of ben_verb_filter_map.txt:
 Adds a field mw=xxx to each line of ben_verb_filter.txt,
indicating the MW root believed to correspond to the BEN root.
For example, aMSay in BEN is believed to correspond to aMS in MW.
;; Case 0001: L=21, k1=aMh, k2=aMh, code=V, mw=aMh
;; Case 0001: L=13, k1=aMSay, k2=aMSay, code=N, mw=aMS

In 6 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0129: L=7404, k1=kAkAy, k2=kAkAy, code=V, mw=?

* ben_upasarga.txt --- not used  --- problem with python regex and unicode
python ben_upasarga.py cae_upasargas.txt ben_upasarga.txt
BEN shows upasargas in bold text, and they are in roman transliteration,
with a few additional wrinkles.
For the big list of upasargas from cae (which are in slp1 transliteration),
construct correspondence from roman to slp1.  This output will be the
initial value of the 'knownupad' dictionary in ben_preverb0.py
We will have to alter this mapping based on the data in ben.
But this initialization just needs to be done once.

* ben_preverb0.txt
python preverb0.py ../ben.txt ben_verb_filter_map.txt ben_upasarga_map.txt ben_preverb0.txt
Note: print statements in 'write' function provide debugging information,
and are thus present in temp_upadump1 file.

For each verb entry of ben.txt, examine the text.
Search for all Devanagari text, and identify the text that represents
one (or more) upasargas.  Determine what is an upasarga by using
ben_upasargas.txt, which lists all distinct upasargas identified for
verbs of cae dictionary, along with additional compound upasargas identified
by visual comparison using the temp_upadump1 file.

For each entry, list the upasargas found therein.
The result will be used to make mw correspondences by preverb1 program .

Sample of first few lines of ben_preverb0.txt
;; Case 0001: L=159, k1=akz, #upasargas=1, upasargas=nis
;; Case 0002: L=360, k1=aNg, #upasargas=0, upasargas=
;; Case 0003: L=403, k1=ac, #upasargas=10, upasargas=anu,ava,A,ud,vyud,samud,ni,pari,vi,sam

* ben_preverb1.txt
python preverb1.py slp1 ben_preverb0.txt ben_verb_filter_map.txt mwverbs1.txt ben_preverb1.txt
python preverb1.py deva ben_preverb0.txt ben_verb_filter_map.txt mwverbs1.txt ben_preverb1_deva.txt



The number of upasargas found is reported on a line for the verb entry.
The first BEN verb entry has no upasargas:
;; Case 0001: L=21, k1=aMh, k2=aMh, code=V, #upasargas=0, mw=aMh (same)

The seventh BEN verb entry has 7 upasargas:
```
;; Case 0007: L=340, k1=ac, k2=ac, code=V, #upasargas=7 (3/4), mw=ac (same)
01        apa         ac                 apAc                 apAc yes apa+ac
02          A         ac                   Ac                   Ac yes A+ac
03         ud         ac                 udac                 udac no 
04         ni         ac                 nyac                 nyac no 
05       pari         ac               paryac               paryac no 
06         vi         ac                 vyac                 vyac yes vi+ac
07        sam         ac                samac                samac no 
```
For each upasarga, an attempt is made to match the prefixed verb to a
known MW prefixed verb.  
In this example, three prefixed forms were found as MW verbs (apAc, Ac, and vyac);
while 4 prefixed forms were not found as MW verbs.

Altogether, there are currently 3099 prefixed forms matched to MW verbs ('yes' cases), 
and 255 'no' cases.


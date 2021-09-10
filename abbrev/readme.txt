Adding ab and ls markup to Benfey.

# Start with temp_ben.txt, which is same as csl-orig/v02/ben/ben.txt at
# commit 35aaf4f9e8e90387384ccf5ded48c2438a4f1ec7
# End with temp_ben_5.txt, which is then pushed to


ben_ls.txt contains tooltips for literary source abbreviations from Benfey front matter.
Format is A = tip
ben_ab.txt contains tooltips for common abbreviations from Benfey front matter.
Format is A = tip

# establish extended ascii characters.  This is used in constructing
# markup.py, so we can control markup of X  (think X='m.') to exclude false
# markup
python ea.py temp_ben.txt ben_ea.txt

# apply markup of 'ab'
python markup.py temp_ben.txt ab ben_ab.txt temp_ben_1.txt ben_ab_stat.txt
# hyphenated ls
There are about 200 ls in which the word is split over 2 lines;
Adjust these as for example:
```
OLD
<div n="lb">Diminution, Man. 1, 70. {@4.@} End, Rā-
<div n="lb">jat. 5, 98. {@5.@} Trespass, injury. {@6.@}
NEW
<div n="lb">Diminution, Man. 1, 70. {@4.@} End,
<div n="lb">Rājat. 5, 98. {@5.@} Trespass, injury. {@6.@}
```
Here are hyphenated prefixes that we will restrict to:
```
 Bhā- 31
 Rā- 102
 Śṛṅ- 3
 Mā- 11
 Mṛ-  1
 Kumā- 1
 Bṛ- 2
 Kā- 1
 Mahā- 1
```
We'll generate a change file, then apply the changes with updateByLine.py
python markup.py temp_ben.txt ab ben_ab.txt temp_ben_1.txt ben_ab_stat.txt

python change_hyphen_ls.py temp_ben_1.txt change_hyphen_ls.txt
python updateByLine.py temp_ben_1.txt change_hyphen_ls.txt temp_ben_2.txt
# multi-word abbreviations on two lines
python change_two_ls.py temp_ben_2.txt ben_ls.txt change_two_ls.txt
python updateByLine.py temp_ben_2.txt change_two_ls.txt temp_ben_3.txt
# apply markup of 'ls'
python markup.py temp_ben_3.txt ls ben_ls.txt temp_ben_4.txt ben_ls_stat.txt
# additional common abbreviations
python markup.py temp_ben_4.txt ab ben_ab2.txt temp_ben_5.txt ben_ab2_stat.txt

# ----------------------------------------------------------------------
integration to rest of system
  of 
# temp_ben_5.txt

cp temp_ben_5.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt

cp ben_ls.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/ben/pywork/
Then make benauth directory, etc.

similarly for ben_ab.txt and ben_ab2.txt.
then make benab directory, etc.

work on issue8 for BEN dictionary.  
objective: Proofread Greekj text.

# *************************************************************************
# startup instructions (for Anna)
# *************************************************************************
# 1. update local copy of BEN repository  
cd to your copy of sanskrit-lexicon/BEN repository
git pull
#  You should now have a BEN/issues/issue8 directory
---------
# 2. sync local copy of csl-orig repository
cd ~/Documents/cologne/csl-orig
git pull
--------
# 3. temp_ben_0.txt
cd ~/Documents/sanskrit-lexicon/ben/issues/issue8
cp ~/Documents/cologne/csl-orig/v02/BEN/ben.txt temp_ben_0.txt
# 4. temp_ben_1.txt
# make a second copy in issue8
cp temp_ben_0.txt temp_ben_1.txt

# *************************************************************** **********
# Make corrections to temp_ben_1.txt
# *************************************************************************
This is the main task.
edit temp_ben_1.txt.
Greek text is identified by '<lang n="greek">X</lang>'.
There are 1265  instances in 1078 lines  of greek text in temp_ben_1.txt.

For each such instance:
 a. compare temp_ben_1.txt to the scanned image of Benp dictionary.
 b. If necessary, make change to temp_ben_1.txt
    NOTE: Do not introduce new (extra) lines in temp_ben_1.txt,
          as this will cause problems in next step



# *************************************************************************
# make change_1.txt
# *************************************************************************
# The program diff_to_changes_dict.py compares each line of
# temp_ben_0.txt to the corresponding line of temp_ben_1.txt.
# If these lines are different (i.e., a change was made in temp_ben_1.txt),
# then the program writes a change transaction.
python diff_to_changes_dict.py temp_ben_0.txt temp_ben_1.txt change_1.txt

Notes:
1. You can remake change_1.txt at any time.
1a. diff_to_changes_dict.py assumes temp_ben_0.txt and temp_ben_1.txt
   have the same number of lines. That's why the 'no extra lines'
   comment above is important.
2. You can push this BEN repository at any time
3. Jim will use his own copy of temp_ben_0.txt and your pushed
   change_1.txt to recreate his copy of your temp_ben_1.txt.
   [See *install instructions* below for details.
4. The BEN/.gitignore file has 'temp*' line, which means
   git will not track files whose names start with 'temp'.
   Thus Anna's local temp_ben_1.txt is not directly available to Jim.
   But Jim can recreate a copy of Anna's temp_ben_1.txt from change_1.txt.


@ list 'slav.' instances in ben.txt
 python extract_slav.py temp_ben_0.txt extract_slav.txt
 select 182 entries matching "slav."
# *************************************************************************
russ.strings.txt, slav.strings.txt, Modified.strings.txt
  Prepared by Andhrabharati
# *************************************************************************

---------------------------------------------------
Modified.strings.txt has just the changes, for Slavonic, russian, and
one arabic.
Some of the differences are hard to discern. Thus,
dump the unicode character information.
python unicode_dump.py Modified.strings.txt Modified.strings_uni.txt
------------------
temp_ben_1.txt
 manual correction of russian in Modified.strings_uni.txt.
# generate change file.
python diff_to_changes_dict.py temp_ben_0.txt temp_ben_1.txt change_1.txt
6 changes written to change_1.txt

# *************************************************************************
temp_ben_2.txt
 manual correction of the modified slavonic strings,
 and 1 arabic string.
python diff_to_changes_dict.py temp_ben_1.txt temp_ben_2.txt change_2.txt
32 changes written to change_2.txt

# *************************************************************************
# Installation of temp_ben_2.txt (Jim)
# *************************************************************************

# install into csl-orig
# a. copy to csl-orig
cp temp_ben_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt

# b. Recreate local displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'ben ' redo_xampp_all.sh
sh generate_dict.sh ben  ../../ben

# c. check xml validity of ben.xml
sh xmlchk_xampp.sh ben
# ok.  [If there are errors, they must be corrected]

## d. update csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .  # v02/ben/ben.txt
git commit -m "ben. russian and slavonic corrections from Modified.strings..
 Ref: https://github.com/sanskrit-lexicon/BEN/issues/5"
git push
----------------------------------------------------
update at Cologne
cd ... csl-orig
git pull
cd ../csl-pywork/v02
grep 'ben ' redo_cologne_all.sh
sh generate_dict.sh ben  ../../BENScan/2020/
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue8
----------------------------------------------------
update this repository
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue8

# *************************************************************************

# *************************************************************************
# THE END
# *************************************************************************

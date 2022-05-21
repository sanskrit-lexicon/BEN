Insertion of Greek text into ben.txt

temp_ben_0.txt   latest from csl-orig:
cp /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt temp_ben_0.txt
  At csl-orig commit baf520659e8f4474eb905ba737695e1d3911b572
  
temp_ben_ab_0.txt Andhrabharati's text
downloaded from link
 https://github.com/sanskrit-lexicon/csl-devanagari/issues/32#issuecomment-1115115483
cp ~/Downloads/BEN_main_L2a.txt greek/temp_ben_ab_0.txt

==============================================================
17312 matches for "^<L>" in buffer: temp_ben_0.txt
17309 matches for "^<L>" in buffer: temp_ben_ab_0.txt

First have to resolve difference in number of headwords.

temp_ben_ab_1.txt
python ab_convert_1.py temp_ben_ab_0.txt temp_ben_ab_1.txt
86985 lines read from temp_ben_ab_0.txt
86985 records written to temp_ben_ab_1.txt

Note:  temp_ben_ab_0.txt and temp_ben_ab_1.txt are the same,
  except for unix line-endings in temp_ben_ab_1.txt.
  

==============================================================
temp_ben_ab_1_slp1.txt : convert Devanagari to slp1.
cd transcode
python deva.py deva,slp1 ../temp_ben_ab_1.txt ../temp_ben_ab_1_slp1.txt
# check invertibility
python deva.py slp1,deva ../temp_ben_ab_1_slp1.txt temp.txt
diff ../temp_ben_ab_1.txt temp.txt | wc -l
# 18 should be 0   See issue #2
 This is 'oM' vs. 'o~' anomaly. mentioned in
  https://github.com/sanskrit-lexicon/BOP/issues/2
==============================================================
temp_ben_ab_2_slp1.txt
1. change o~ to oM  6 matches in 4 lines, L=516, L=3814
2. Change ' <LEND>' '<LEND>' (at L=1294)

temp_ben_1.txt  
python prep1.py temp_ben_0.txt temp_ben_ab_2_slp1.txt temp_prep1.txt
3 L present in temp_bur_0 but not temp_bur_ab_2:
  {'7323', '5697', '2866'}
AB note:
; <L>2866 is wrongly split as a diff. HW, and is merged properly with <L>2865.
 kaccid merged into kad
; <L>5697 is wrongly split as a diff. HW, and is merged properly with <L>5696.
 tantrita merged into tantri
; <L>7323 is wrongly split as a diff. HW, and is merged properly with <L>7322.
 nABI merged into nABi

Also, change page number at L=15491, saMdeha from '1003-a' to '1003-b'.

python prep1.py temp_ben_1.txt temp_ben_ab_2_slp1.txt temp_prep1.txt
787 entries with Greek phrases in csl
783 entries with Greek phrases in ab
208 entries with different number of greek phrases
788 records written to temp_prep1.txt
208 entries with differences to resolve


temp_ben_2.txt
 many cases where Greek text spreads over two lines
 first line ends with <lang n="greek"></lang> and
 second lines starts with same.  However, the ben_ab version shows only
 one greek text .
 Temporarily, change second line to <xlang n="greek"></lang>

python change_xlang.py temp_ben_1.txt change_2.txt
236 changes
python updateByLine.py temp_ben_1.txt change_2.txt temp_ben_2.txt

python prep1.py temp_ben_2.txt temp_ben_ab_2_slp1.txt temp_prep2.txt
788 records written to temp_prep2.txt
40 entries with differences to resolve

Manual changes resolving the differences lead to 
temp_ben_3.txt and temp_ben_ab_3_slp1.txt

python prep1.py temp_ben_3.txt temp_ben_ab_3_slp1.txt temp_prep2_3.txt
784 records written to temp_prep2_3.txt
0 entries with differences to resolve

python diff_to_changes.py temp_ben_2.txt temp_ben_3.txt change_3.txt
60 changes

python diff_to_changes.py temp_ben_ab_1_slp1.txt temp_ben_ab_2_slp1.txt change_ab_2.txt
5 changes
python diff_to_changes.py temp_ben_ab_2_slp1.txt temp_ben_ab_3_slp1.txt change_ab_3.txt
3 changes
L=14998:  κρανρος is likely wrong at ν (line # 75597 missing text)
see change_ab_3.txt.

==============================================================
sequentially insert Greek language text instances from ben_ab to ben
python change_insert_ab.py temp_ben_3.txt temp_ben_ab_3_slp1.txt change_4.txt
len(changes)= 1057
1057 changes written to change_4.txt

python updateByLine.py temp_ben_3.txt change_4.txt temp_ben_4.txt

==============================================================
1243 matches in 1057 lines for "<lang n="greek">[^<]+?</lang>" in buffer: temp_ben_4.txt

There are 22 unfilled greek text fragments in the ADDENDA AND CORRIGENDA	 section.

1243 matches in 808 lines for "<lang n="greek">[^<]+?</lang>" in buffer: temp_ben_ab_3_slp1.txt
  So CSL and AB versions have same number of greek text fragments.

==============================================================
temp_ben_5.txt  remove '<xlang n="greek"></lang>'
  cp temp_ben_4.txt temp_ben_5.txt
  manuallly '^ *<xlang n="greek"></lang> *' -> ''
  243 lines changed.
  
==============================================================
install into csl-orig and check validity
cp temp_ben_5.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ben  ../../ben
sh xmlchk_xampp.sh ben
  OK as hoped!

cd /c/xampp/htdocs/sanskrit-lexicon/ben/greek

==============================================================
Prepare document for proofreading the greek.

This can be applied to different language names
python proof.py greek temp_ben_5.txt proof_greek.txt

==============================================================
temp_ben_6.txt
two additional corrections,
  Ref: https://github.com/sanskrit-lexicon/BEN/issues/6#issuecomment-1133194534
   and next comment
python diff_to_changes.py temp_ben_5.txt temp_ben_6.txt change_6.txt
2 changes
python proof.py greek temp_ben_6.txt proof_greek.txt

install into csl-orig and check validity
cp temp_ben_6.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ben  ../../ben
sh xmlchk_xampp.sh ben
  OK as hoped!

cd /c/xampp/htdocs/sanskrit-lexicon/ben/greek

==============================================================
punctuation
Often, the punctuation character following the Greek text
is missing in csl version.
python punct.py temp_ben_6.txt temp_ben_ab_3_slp1.txt change_7.txt
744 changes

python updateByLine.py temp_ben_6.txt change_7.txt temp_ben_7.txt

install into csl-orig and check validity
cp temp_ben_7.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ben  ../../ben
sh xmlchk_xampp.sh ben
  OK as hoped!


cd /c/xampp/htdocs/sanskrit-lexicon/ben/greek
python proof.py greek temp_ben_7.txt proof_greek.txt
==============================================================

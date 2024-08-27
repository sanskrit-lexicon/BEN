
Begin 08-26-2024

Ref: https://github.com/sanskrit-lexicon/BEN/issues/9
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/ben/ben.txt at commit
  2a225bbfff972baf0f53afb8ebfbebe77ca02bf7


# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_ben_0 .txt in this directory
  git show  2a225bbff:v02/ben/ben.txt > /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9/temp_ben_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9
------
# similarly copy ben_hwextra from csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/
git show  2a225bbff:v02/ben/ben_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9/ben_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

---------------------------------
temp_ben_1.txt, ben_front.txt, ben_back.txt
Extract lines before first entry into ben_front.txt
Extract lines after last entry into ben_back.txt
Remove blank lines in the remaining, and write to temp_ben_1.txt

python frontback.py temp_ben_0.txt temp_ben_1.txt ben_front.txt ben_back.txt


--------------------------------------------------------
temp_ben_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_ben_1.txt temp_ben_2.txt

Notes:
1. there are no <info /> tags in benfey as of now.
2. [Pagexxx] lines (between entries) are dropped in temp_ben_2

--------------------------------------------------------
temp_ben_3.txt

python convert_hwextra_lbody.py temp_ben_2.txt ben_hwextra.txt temp_ben_3.txt
129055 lines read from temp_ben_2.txt
17309 entries found
1 from ben_hwextra.txt
17310 records written to temp_ben_3.txt

There is only one item in ben_hwextra.txt:
<L>1689.1<k1>Arti<k2>Arti<type>alt<LP>1689<k1P>Artti

--------------------------------------------------------
Version PRIOR to changes.  benhwx  (uses ben_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ben ../../benhwx

cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

--------------------------------------------------------
revise hw.py
/c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'ben' to the 'Lbody' list.
--------------------------------------------------------
Version using {{LBody=N}}
cp temp_ben_3.txt /c/xampp/htdocs/cologne/csl-orig/v02/ben/ben.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
 grep 'ben ' redo_xampp_all.sh
sh generate_dict.sh ben  ../../ben
sh xmlchk_xampp.sh ben
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

--------------------------------------------------------
revise csl-orig/v02/ben
mkdir althws
mv ben_hwextra.txt althws/
touch ben_hwextra.txt
edit althws/readme.txt

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   ben/ben.txt
        modified:   ben/ben_hwextra.txt

        Untracked files:
        (use "git add <file>..." to include in what will be committed)
        ben/althws/
git add .
git commit -m "BEN: Lbody groups.
Ref: https://github.com/sanskrit-lexicon/BEN/tree/master/issues/issue9"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .
git commit -m "BEN: Lbody groups.
Ref: https://github.com/sanskrit-lexicon/BEN/tree/master/issues/issue9"

git push
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

-------------------------------------
install revised ben on Cologne server

cd csl-orig
git pull

# revise displays for ben
cd csl-pywork/v02
git pull

sh generate_dict.sh ben  ../../BENScan/2020/

-----------------------
Sync this BEN repo
cd /c/xampp/htdocs/sanskrit-lexicon/BEN/issues/issue9

git status
        new file:   ben_back.txt
        new file:   ben_front.txt
        new file:   ben_hwextra.txt
        new file:   convert_hwextra_lbody.py
        new file:   digentry.py
        new file:   frontback.py
        new file:   info_end.py
        new file:   infotag.py
        new file:   infotag_attr.txt
        new file:   infotag_notend.txt
        new file:   readme.txt


git add .
git commit -m "finish Lbody for groups #34  "
=========================================================


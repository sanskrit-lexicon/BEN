ben_main_L2a.txt file is provided by Andhrabharati on 02 May 2022 at <https://github.com/sanskrit-lexicon/csl-devanagari/issues/32#issuecomment-1115115483>.
ben_addenda.txt file is provided by Andhrabharati on 18 February 2022 at <https://github.com/sanskrit-lexicon/BEN/issues/5#issuecomment-1044573674>.
They may have been taken some days back from CDSL and enriched by Andhrabharati.
We may need to find out a way to integrate changes in CDSL data made from around December 2021 and merge CDSL and AB version.
32601aaa27fae7d7710540ff968df41a6f913700 is the commit in csl-orig/v02/ben/ben.txt of 16 December 2021. Start to see from there.

Occurrence of Kriṣṇa in ben_Main_L2.txt means that it was taken before 03 October 2021 commit 0cbf4fa8489a7a3694479a8319fa8e5dc67419bb.

Going backwards, b4f5ddd in csl-orig seems to be the commit on which the first csl-devanagari version was created on 03 September 2021.
We take this as the base for now.

# csl-devanagari file

cd /path/to/csl-devanagari
mkdir -p slp1
mkdir -p diff
cd scripts
sh redo.sh ben

This regenerates the ben (Devanagari version) from csl-orig in v02/ben/ben.txt.
Date of taking 29 June 2026.

cp v02/ben/ben.txt /path/to/BEN/issues/issue5/temp_base_ben.txt

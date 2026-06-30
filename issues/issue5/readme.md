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

# Align CDSL version and AB version

```
cd /path/to/BEN/issues/issue5
sh redo.sh
```

This runs 3 scripts:
`step1.py`: CDSL transformations + AB normalization
`step2.py`: abbreviation tagging.
`step3.py`: page line numbers into AB

At the end of the three scripts, we get two files

`derivatives/temp_cdsl_ben3.txt` and `derivatives/temp_ab_ben3.txt`.

Analyse the differences by

`vimdiff derivatives/temp_cdsl_ben3.txt derivatives/temp_ab_ben3.txt`

These are mainly cases where there are genuine differences between CDSL and AB version. Noise has been weeded out.

# Transfer the changes to csl-devanagari repo

As AB had worked with Devanagari version of the file, we need to transfer the changes to csl-devanagari repo first.

### Add step1 output to csl-devanagari

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
cp /Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue5/derivatives/temp_cdsl_ben1.txt v02/ben/ben.txt
git diff --word-diff-regex=.
git status
git add .
git commit -m 'CDSL version modified to suit AB version. See step1 https://github.com/sanskrit-lexicon/BEN/issues/5'
git push
```

### Add step2 output to csl-devanagari

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
cp /Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue5/derivatives/temp_cdsl_ben2.txt v02/ben/ben.txt
git diff --word-diff-regex=.
git status
git add .
git commit -m 'CDSL version modified to suit AB version. See step2 https://github.com/sanskrit-lexicon/BEN/issues/5'
git push
```

### Add AB version L2 to csl-devanagari

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
cp /Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue5/derivatives/temp_ab_ben1.txt v02/ben/ben.txt
git diff --word-diff-regex=.
git status
git add .
git commit -m 'AB version added. See https://github.com/sanskrit-lexicon/BEN/issues/5'
git push
```

### Add step3 output to csl-devanagari

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
cp /Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue5/derivatives/temp_ab_ben3.txt v02/ben/ben.txt
git diff --word-diff-regex=.
git status
git add .
git commit -m 'Line counts added after page number in AB version. See https://github.com/sanskrit-lexicon/BEN/issues/5'
git push
```

### Add BEN_Main_L2a.txt data

This file had 15 differences from ben_Main_L2.txt file. step1.py was modified to use BEN_Main_L2a.txt file as input and `redo.sh` was run, generating the file temp_ab_ben3.txt incorporating all the 15 changes.
This may not be required to be run, as for any fresh run, redo.sh step would take care of it. Just noting it here for historic purposes.

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
git add .
git commit -m 'Chages between ben_Main_L2 and BEN_main_L2a incorporated. See https://github.com/sanskrit-lexicon/BEN/issues/5'
git push
```

# Carry changes from csl-devanagari to csl-orig repo

```
cd /Users/Shared/csl-devanagari
cd scripts
python to_slp1.py ben
cp ../slp1/ben.txt ../../csl-orig/v02/ben/ben.txt
```

# Add the changes to csl-orig repo

```
cd /Users/Shared/csl-orig
git add .
git commit -m 'BEN as per AB version L2a. See https://github.com/sanskrit-lexicon/BEN/issues/5 and https://github.com/sanskrit-lexicon/csl-devanagari/issues/32'
git push
```

# Manual changes to csl-orig/v02/ben/ben.txt

When tried to push to the csl-orig repo, there were a few fromatting errors which raised malformed XML errors.
They three items were manually corrected in csl-orig/v02/ben/ben.txt

```
diff /Users/Shared/sanskrit-lexicon/csl-devanagari/slp1/ben.txt /Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt
6173c6173
<  <LEND>
---
> <LEND>
39389c39389
< 1. {#nu#}¦ {%nu%}, and {#nU#} {%nū%}, <ab>ved.</ab> (perhaps akin to {%nava%}, <ab>cf.</ab> {%nūtana%}), a particle, {@1.@} Now (<ab>ved.</ab>). {@2.@} A particle of interrogation in two or more interrogative sentences succeeding each other, <ls>Śāk.</ls> <ab>d.</ab> 137. {@3.@} Preceded by interrogatives, <ls>MBh.</ls> 5, 6003. {@4.@} {%nu--nu%}, Either... or, <ls>Rām.</ls> 2, 72, 27; {%nu--nu--nu... or...or, <ls>Kir.</ls> 5. 1. {@5.@} A <ab>part.</ab> of affirmation, Indeed, <ls>Chr.</ls> 291, 13 = <ls>Rigv.</ls> i. 64, 13.
---
> 1. {#nu#}¦ {%nu%}, and {#nU#} {%nū%}, <ab>ved.</ab> (perhaps akin to {%nava%}, <ab>cf.</ab> {%nūtana%}), a particle, {@1.@} Now (<ab>ved.</ab>). {@2.@} A particle of interrogation in two or more interrogative sentences succeeding each other, <ls>Śāk.</ls> <ab>d.</ab> 137. {@3.@} Preceded by interrogatives, <ls>MBh.</ls> 5, 6003. {@4.@} {%nu--nu%}, Either... or, <ls>Rām.</ls> 2, 72, 27; {%nu--nu--nu%} ... or ... or, <ls>Kir.</ls> 5. 1. {@5.@} A <ab>part.</ab> of affirmation, Indeed, <ls>Chr.</ls> 291, 13 = <ls>Rigv.</ls> i. 64, 13.
75671c75671
<  --<ab>Cf.</ab> {%śaraṇa%}, and <ab>Goth.</ab> hulth; <ab>A.S.</ab> hold; perhaps <ab>Goth.</ab> hail; <ab>A.S.</ab> hál; perhaps <ab>Lat.</ab> clemens; to the original signification seem to belong, <lang n="greek">κλίνω, κλισία, κλιτύς; <ab>Lat.</ab> in-clinare, clivus; <ab>Goth.</ab> hlains, hleithra, hlija; <ab>A.S.</ab> hlynian, hlidh.
---
>  --<ab>Cf.</ab> {%śaraṇa%}, and <ab>Goth.</ab> hulth; <ab>A.S.</ab> hold; perhaps <ab>Goth.</ab> hail; <ab>A.S.</ab> hál; perhaps <ab>Lat.</ab> clemens; to the original signification seem to belong, <lang n="greek">κλίνω, κλισία, κλιτύς</lang>; <ab>Lat.</ab> in-clinare, clivus; <ab>Goth.</ab> hlains, hleithra, hlija; <ab>A.S.</ab> hlynian, hlidh.
```

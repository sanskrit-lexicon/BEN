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
`step4.py`: Add Greek tags from CDSL to AB version, as CDSL greek tags are proof-read.

At the end of the four scripts, we get two files

`derivatives/temp_cdsl_ben3.txt` and `derivatives/temp_ab_ben4.txt`.

Analyse the differences by

`vimdiff derivatives/temp_cdsl_ben3.txt derivatives/temp_ab_ben4.txt`

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

### Add step4 output to csl-devanagari

```
cd /Users/Shared/sanskrit-lexicon/csl-devanagari
cp /Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue5/derivatives/temp_ab_ben3.txt v02/ben/ben.txt
git diff --word-diff-regex=.
git status
git add .
git commit -m 'Greek tags reintroduced from CDSL version. See https://github.com/sanskrit-lexicon/BEN/issues/5'
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

# Manually add changes made to csl-orig/v02/ben/ben.txt from September 2021 to June 2026

Studied the history of changes to csl-orig/v02/ben/ben.txt file by looking at <https://github.com/sanskrit-lexicon/csl-orig/commits/main/v02/ben/ben.txt>.
It is not sure when the file was taken by Andhrabharati.
Therefore, a guess was made.
Occurrence of 'ἄρκτος' in BEN_Main_L2a.txt suggests that it was taken after <https://github.com/sanskrit-lexicon/csl-orig/commit/6f4d89c1d5f28070d565140f922bff4b4907c08b> and presence of 'Kriṣṇa' suggests that it was taken before <https://github.com/sanskrit-lexicon/csl-orig/commit/2cdcc5e720865413c4308a068fbbb9a21944c086>.

Therefore, the following commits were checked for any changes which may have been made in csl-orig after the file was taken by AB i.e. commit 6f4d89c1d5f28070d565140f922bff4b4907c08b

```
338005a BEN corrections per #745
e2ed7bb BEN: trim trailing space inside <lang n="greek"> at line 58227
2a9adf2 AP, AP90, BEN, BHS update for printchanges
3b990c8 chh->ch. close #197
ad874b2 BEN ring above
2e04143 BEN changes per https://github.com/sanskrit-lexicon/csl-corrections/issues/75
a7e3461 BEN, PWG  drohin. Ref: https://github.com/sanskrit-lexicon/PWG/issues/135#issuecomment-2857066545
090fa03 BEN: Lbody groups. Ref: https://github.com/sanskrit-lexicon/BEN/tree/main/issues/issue9
7a627f2 BEN. L=6526  'du' Ref: https://github.com/sanskrit-lexicon/BEN/issues/8
de40d4d BEN. greek Proofreading  Ref: https://github.com/sanskrit-lexicon/BEN/issues/8
293922d BEN: Greek text in addenda. Ref: https://github.com/sanskrit-lexicon/BEN/issues/6
9cc52c9 BEN: punctuation after greek text fragments. Ref: https://github.com/sanskrit-lexicon/BEN/issues/6
f55236e BEN: 2 additional greek corrections.
4a2dbf7 BEN: Greek text added. Ref: https://github.com/sanskrit-lexicon/BEN/issues/6
32601aa BEN: remove <div n='lb'> markup. Ref: https://github.com/sanskrit-lexicon/csl-devanagari/issues/26
d28a8af BEN: insert <div n='lb'> at lines starting with '<lang'.  This in preparation for removing all <div n='lb'>. Ref https://github.com/sanskrit-lexicon/csl-devanagari/issues/26
5f62bda handled suggestion made in https://github.com/sanskrit-lexicon/csl-orig/issues/633#issuecomment-932992049
0cbf4fa typo correction
2cdcc5e BEN corrections. Ref: https://github.com/sanskrit-lexicon/csl-devanagari/issues/33
```

They were manually corrected in csl-orig/v02/ben/ben.txt

```
commit 447359963158cfd494d3a2285ddccf1a0bbfd83b (HEAD -> main, origin/main, origin/HEAD)
Author: Dr. Dhaval Patel <drdhaval2785@gmail.com>
Date:   Tue Jun 30 14:37:02 2026 +0530

    csl-orig corrections from the diverging commit carried back into AB which is now on CDSL. See https://github.com/sanskrit-lexicon/BEN/issues/5

```

Correct error in conversion of 'Sh,sh' to 'Ṣṣ'.
Ref: https://github.com/sanskrit-lexicon/csl-devanagari/issues/32

Ṣṣ are assumed correct if in {%X%}.  This assumption works for Benfey.

#---------------------------------------------------
Generate a frequency list of all words that contain Ṣṣ.
Exclude {%X%} (italic - Sanskrit)
 <ls>X</ls>   (literary source)
 <ab>X</ab>   (abbreviations)
 <x>  xml tags

cp ../ben.txt temp_ben0.txt
python shwords.py temp_ben0.txt shwords.txt
119 words

Separate into shwords_ok.txt and shwords_wrong.txt
Differences from AB:
I Do not count as wrong:
<div n="lb">A creeper, commonly Ghoṣā.
   This is a Sanskrit word acc. to MW, although not italicized in Benfey.
<div n="lb">A tree, Mimosa siriṣa.
  hw BaRqila change to śirīṣa for consistency (print change)
<div n="lb">Mimosa śirīṣa. {@3.@} The name of a mUzika
  The ī suggests this is not a 'scientific' name;  It is a Sanskrit word acc. to MW.
  

# generate correction transactions for wrong words
# 23 changes
python change1.py temp_ben0.txt shwords_wrong.txt temp_change1.txt
 change1.txt start same as temp_change1.txt, manually
 correct one false positive for 'ṣa'
 
pcerr.txt
 prepared for generating <pc> corrections of metalines
python changepc.py temp_ben0.txt pcerr.txt temp_changepc.txt
# add these to change1.txt
Then apply
python updateByLine.py temp_ben0.txt change1.txt temp_ben1.txt
180 lines changed
Now install temp_ben1.txt into csl-orig/v02/ben/ben.txt

# Step 1

1. `https://github.com/sanskrit-lexicon/csl-devanagari/files/7272000/ben_Main.txt` copied as `ben_ab0.txt`. This file will not be changed.
2. Keep the file https://github.com/sanskrit-lexicon/csl-devanagari/blob/main/v02/ben/ben.txt as it existed as on 30 September 2021 as a base file. This is the file from which Andhrabharati corrected / modified his version. Commit was d545400f309906d807155e5baa4fabfb24fe8048. 
```
cd ../../../cologne/csl-devanagari/
git show d545400f309906d807155e5baa4fabfb24fe8048:v02/ben/ben.txt > ../../cologne-extra/BEN/ben_ab/ben_cologne0.txt
```
This file will also not be changed.
3. `python3 ab_analysis.py`. This will generate the following files.
4. `ben_ab1.txt` - AB text with all content on one line per entry.
5. `ben_cologne1.txt` - Cologne text with all content on one line per entry.
6. `ben_ab2.txt` - AB text with adjustment for comparability with Cologne text.
7. `ben_cologne2.txt` - Cologne text with adjustment for comparability with AB text.
8. `wdiff -n ben_ab2.txt ben_cologne2.txt | grep '{+' | wc -l` will calculate the number of different lines between two versions.
9. Tweak program `ab_analysis.py`to smoothen out as many differences as possible.

# Statistics



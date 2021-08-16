
For english word corrections, the final results are in files:
 ben_error_ok_lang.txt
 ben_error_todo5.txt.
These files were derived from ben_error.txt in several steps,
 some programmatic, and some manual.

----------------------------------------------------------------
Use whitaker/latinwords.txt to mark ben_error.txt items as Latin.

python mark_lang.py Latin ben_error.txt whitaker/latinwords.txt ben_error_latin.txt ben_error_todo.txt

python benlang.py 'Lat.' temp_ben.txt benlang_latin_raw.txt
; manually edit to get benlang_latin.txt
python edit1.py 'Lat.' benlang_latin_1.txt benlang_latin.txt
; extract words
python edit1a.py 'Lat.' benlang_latin.txt ben_latinwords.txt

# further reduce the ben_error suggestions

python mark_lang.py Latin ben_error_todo.txt ben_latinwords.txt ben_error_latin1.txt ben_error_todo1.txt

Now work with Goth. words

python benlang.py 'Goth.' temp_ben.txt benlang_goth_raw.txt
edit benlang_goth_1.txt  (starts as .._raw)
separate out words
python edit1.py 'Goth.' benlang_goth_1.txt benlang_goth.txt
python edit1a.py 'Goth.' benlang_goth.txt ben_gothwords.txt
 557
python mark_lang.py 'goth' ben_error_todo1.txt ben_gothwords.txt ben_error_goth1.txt ben_error_todo2.txt


Anglo-Saxon
Change A. S. to A.S.
python benlang.py 'A.S.' temp_ben.txt benlang_angsax_raw.txt
edit benlang_angsax_1.txt  (starts as .._raw)
separate out words
python edit1.py 'A.S.' benlang_angsax_1.txt benlang_angsax.txt
python edit1a.py 'A.S.' benlang_angsax.txt ben_angsaxwords.txt
 662
python mark_lang.py 'AS' ben_error_todo2.txt ben_angsaxwords.txt ben_error_angsax1.txt ben_error_todo3.txt

Old High German
Change O. H. G. to O.H.G.

python benlang.py 'O.H.G.' temp_ben.txt benlang_ohg_raw.txt
edit benlang_ohg_1.txt  (starts as .._raw)
separate out words
python edit1.py 'O.H.G.' benlang_ohg_1.txt benlang_ohg.txt
python edit1a.py 'O.H.G.' benlang_ohg.txt ben_ohgwords.txt
 495
python mark_lang.py 'OHG' ben_error_todo3.txt ben_ohgwords.txt ben_error_ohg1.txt ben_error_todo4.txt


Manually, from ben_error_todo4:
ben_error_misc.txt
ben_error_todo5.txt  (for sampada)

cat ben_error_latin.txt ben_error_latin1.txt ben_error_angsax1.txt ben_error_goth1.txt  ben_error_ohg1.txt ben_error_misc.txt > ben_error_ok_lang.txt
  1867 items from ben_error.txt that have been marked by Jim
ben_error_todo5.txt
  133 items from ben_error.txt that are unmarked.  For Sampada.





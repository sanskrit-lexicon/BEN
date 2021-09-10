python markup.py temp_ben.txt ab ben_ab.txt temp_ben_1.txt ben_ab_stat.txt

python change_hyphen_ls.py temp_ben_1.txt change_hyphen_ls.txt
python updateByLine.py temp_ben_1.txt change_hyphen_ls.txt temp_ben_2.txt
# multi-word abbreviations on two lines
python change_two_ls.py temp_ben_2.txt ben_ls.txt change_two_ls.txt
python updateByLine.py temp_ben_2.txt change_two_ls.txt temp_ben_3.txt
python markup.py temp_ben_3.txt ls ben_ls.txt temp_ben_4.txt ben_ls_stat.txt
#
python markup.py temp_ben_4.txt ab ben_ab2.txt temp_ben_5.txt ben_ab2_stat.txt

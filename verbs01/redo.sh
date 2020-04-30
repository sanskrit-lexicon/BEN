echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake ben_verb_filter.txt"
python ben_verb_filter.py ../ben.txt  ben_verb_exclude.txt ben_verb_filter.txt
echo "remake ben_verb_filter_map.txt"
python ben_verb_filter_map.py ben_verb_filter.txt mwverbs1.txt ben_verb_filter_map.txt
echo "remake ben_preverb0"
python preverb0.py ../ben.txt ben_verb_filter_map.txt ben_upasarga_map.txt ben_preverb0.txt


echo "remake ben_preverb1.txt"
python preverb1.py slp1 ben_preverb0.txt ben_verb_filter_map.txt mwverbs1.txt ben_preverb1.txt
echo "remake ben_preverb1_deva.txt"
python preverb1.py deva ben_preverb0.txt ben_verb_filter_map.txt mwverbs1.txt ben_preverb1_deva.txt


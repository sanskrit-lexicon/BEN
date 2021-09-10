## Adding ab and ls markup to Benfey.

Brief description of files

## abbreviation data files
* ben_ab.txt Common abbreviations from Benfey front matter
* ben_ls.txt Literary source abbreviations from Benfey front matter
* ben_ab2.txt Additional common abbreviations, not in front matter

## abbreviation data files with approximate frequencies
* ben_ab2_stat.txt
* ben_ls_stat.txt
* ben_ab_stat.txt

## abbreviation files from front matter
Transcription of relevant front matter, plus editing and correction
Used as basis of above files
* ben_abwork.txt  
* ben_abwork_edit.txt

## programs and intermediate files
* ben_ea.txt   Extended ascii characters in ben.txt.  Used in markup.py
* ea.py        Program that creates ben_ea.txt

* change_hyphen_ls.txt  Change transactions for hyphenated abbreviations
* change_hyphen_ls.py   Program to generate preceding

* change_two_ls.txt  Change transactions to deal with multiword abbreviations
  appearing on two lines
* change_two_ls.py   Program to generate preceding

* updateByLine.py Utility program to apply one of the change transaction files
  to a version of the digitization, thereby getting a revised digitization.
  
* markup.py Program to add markup to a version of ben.txt based on one of the abbreviation files.  Generates a revised version of digitization.
  Also generates the 'stat' files above
  
* readme.txt    Technical notes regarding running the above programs.

* redo.sh  Useful script for redoing the steps required to generate version
  of digitization with ab, ls markup



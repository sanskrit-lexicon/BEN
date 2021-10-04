# This Python file uses the following encoding: utf-8
"""
Usage:
python ab_analysis.py
"""
from __future__ import print_function
import re
import codecs
import os

def oneline_per_entry(inputfile, outputfile):
    fin = codecs.open(inputfile, 'r', 'utf-8')
    fout = codecs.open(outputfile, 'w', 'utf-8')
    start = False
    end = False
    for lin in fin:
        if lin.startswith('<L>'):
            start = True
            end = False
            result = lin
        elif lin.startswith('<LEND>'):
            end = True
            result += '\n' + lin
            fout.write(result)
        elif start and (not end):
            result += lin.rstrip()
    fin.close()
    fout.close()


def adjust_ab(inputfile, outputfile):
    fin = codecs.open(inputfile, 'r', 'utf-8')
    fout = codecs.open(outputfile, 'w', 'utf-8')
    for lin in fin:
        if lin.startswith('<L>') or lin.startswith('<LEND>'):
            fout.write(lin)
        else:
            lin = lin.replace('<lang n="greek">???</lang>', '<lang n="greek"></lang>')
            lin = re.sub('<ls>(.*?)</ls>', '\g<1>', lin)
            lin = re.sub('<ab>(.*?)</ab>', '\g<1>', lin)
            fout.write(lin)
    fin.close()
    fout.close()
    

def adjust_cologne(inputfile, outputfile):
    fin = codecs.open(inputfile, 'r', 'utf-8')
    fout = codecs.open(outputfile, 'w', 'utf-8')
    for lin in fin:
        if lin.startswith('<L>') or lin.startswith('<LEND>'):
            fout.write(lin)
        else:
            lin = lin.replace('-<div n="lb">', '')
            lin = lin.replace('<div n="lb">', ' ')
            lin = lin.replace(',%}', '%},')
            lin = lin.replace('.%}', '%}.')
            lin = lin.replace('{@ -- <ab>Comp.</ab>@} ', '--<ab>Comp.</ab> ¦ ')
            lin = lin.replace('<ab>Ptcple.</ab>', '--<ab>Ptcple.</ab>')
            lin = lin.replace('<ab>Caus.</ab>', '--<ab>Caus.</ab>')
            lin = lin.replace('-- <ab>Cf.</ab>', '--<ab>Cf.</ab>')
            lin = lin.replace('-- With', '--With')
            lin = lin.replace('{#†', '†{#')
            lin = lin.replace('-%} {%', '')
            lin = re.sub('<ls>(.*?)</ls>', '\g<1>', lin)
            lin = re.sub('<ab>(.*?)</ab>', '\g<1>', lin)
            fout.write(lin)
    fin.close()
    fout.close()


if __name__ == "__main__":
    ab0 = 'ben_ab0.txt'
    ab1 = 'ben_ab1.txt'
    ab2 = 'ben_ab2.txt'
    col0 = 'ben_cologne0.txt'
    col1 = 'ben_cologne1.txt'
    col2 = 'ben_cologne2.txt'
    print("Step 1. Create one line per entry ben_ab1.txt and ben_cologne1.txt.")
    oneline_per_entry(ab0, ab1)
    oneline_per_entry(col0, col1)
    print("Step 2. Adjust ben_ab1.txt and ben_cologne1.txt, and generate ben_ab2.txt and ben_cologne2.txt.")
    adjust_ab(ab1, ab2)
    adjust_cologne(col1, col2)

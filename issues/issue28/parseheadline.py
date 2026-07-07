# coding=utf-8
from __future__ import print_function
import sys
import re
if sys.version_info[0] > 2:
    xrange = range

def parseheadline(headline):
    headline = headline.strip()
    splits = re.split('[<]([^>]*)[>]([^<]*)', headline)
    result = {}
    for i in xrange(len(splits)):
        if i % 3 == 1:
            result[splits[i]] = splits[i+1]
    return result

def test():
    testlines = [
        "<L>26<pc>0002-b<k1>akza<k2>akza",
        "<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1<e>2",
    ]
    for line in testlines:
        print(parseheadline(line))

if __name__ == "__main__":
    test()

#!/usr/bin/env python

import sys
import os
import glob
import shutil

_dir = sys.argv[1]
for subdir in os.listdir(_dir):
    fnpat = os.path.join(_dir, subdir, "*[4567].svg")
    files = glob.glob(fnpat)
    if len(files) == 0:
        continue
    files.sort()
    outfn = os.path.join("frames", subdir + "_frames.svg")
    cmd = "python frameit.py %s %s" % (outfn, str.join(' ', files))
    print cmd
    os.system(cmd)

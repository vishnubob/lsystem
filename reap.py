#!/usr/bin/env python

import sys
import os
import glob
import shutil

_dir = sys.argv[1]
for subdir in os.listdir(_dir):
    fnpat = os.path.join(_dir, subdir, "*.svg")
    files = glob.glob(fnpat)
    if len(files) == 0:
        continue
    sz = sum(os.stat(fn).st_size for fn in files)
    if sz < 10000:
        path = os.path.join(_dir, subdir)
        shutil.rmtree(path)
        print path

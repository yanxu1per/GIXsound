'''
@function: create folders for different audio data
'''

from os import makedirs, path
import sys

for i in range(0,72):
    fname = str(i*5)
    newpath = path.join(sys.path[0], fname)
    print newpath
    if not path.exists(newpath):
        makedirs(newpath)

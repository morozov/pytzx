#!/usr/bin/env python3
#
# Simple script to convert a binary file into a packed string
#
import sys

if len(sys.argv) !=2:
    print("Usage: " + sys.argv[0] + " <file>")
else:
    f = open (sys.argv[1], "rb")
    h = f.read()
    sys.stdout.write('binary = \\\n')
    q = - 1
    for byte in range (0, len(h)):
        q = q + 1
        if (q == 0):
            sys.stdout.write('    b\"')
        sys.stdout.write("\\x%02X" % h[byte])
        if (q == 16):
            sys.stdout.write('\" \\\n')
            q = -1
    sys.stdout.write('\"\n')
    f.close()

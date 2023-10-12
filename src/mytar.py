#! /usr/bin/env python3

import sys, re, os, subprocess

if len(sys.argv) < 3:
    print("Invalid formatting.\n")
    print("Valid formatting is either: \n./mytar.py c <file1> <file2>...")
    print("Or:\n./mytar.py x <file1> <file2>...")
    exit()

    
progName = sys.argv[0]
usage = sys.argv[1]
filenames = sys.argv[2:]


from buf import BufferedFdWriter, BufferedFdReader, bufferedCopy

byteWriter = BufferedFdWriter(1)


class Framer():
    print("Framer")
    for filename in filenames:
        with open(filename, 'rb') as rf:
            rf_contents = rf.read(100)
            print(rf_contents)
            while len(rf_contents) > 0:
                rf_contents = rf.read(100)
                




class Unframer():
    print("Unframer")
            



if usage == 'c':
    Framer()


elif usage == 'x':
    Unframer()


else:
    print("Invalid formatting.\n")
    print("Valid formatting is either: \n./mytar.py c <file1> <file2>...")
    print("Or:\n./mytar.py x <file1> <file2>...")



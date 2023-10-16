#! /usr/bin/env python3

import sys, re, os, subprocess

# Catch improper use of program and inform the user
if len(sys.argv) < 3:
    print("Invalid formatting.\n")
    print("Valid formatting is either: \n./mytar.py c <file1> <file2>...")
    print("Or:\n./mytar.py x <tarFile>")
    exit()


progName = sys.argv[0]
usage = sys.argv[1]


from buf import BufferedFdWriter, BufferedFdReader, bufferedCopy

byteWriter = BufferedFdWriter(1)


class Framer:
    def __init__(self, writer):
        self.writer = writer
    def inputByte(self, byte):
        if byte == ord('/'):
            self.writer.writeByte(byte)
        self.writer.writeByte(byte)
    def inputByteArray(self, byteArray):
        for byte in byteArray:
            self.inputByte(byte)
    def end(self):
        # using inband framing with '/e' to seperate filename from contents
        self.writer.writeByte(ord('/'))
        self.writer.writeByte(ord('e'))
        self.writer.flush()
            


class Unframer:
    def __init__(self, reader):
        self.reader = reader
    def checkByte(self, byte):
        if byte == ord('/'):
            nextByte = self.reader.readByte()
            if nextByte == ord('e'):
                return False
        return True
    def readByteArray(self):
        byteArray = bytearray()
        # Loop through and 
        while True:
            byteVal = self.reader.readByte()
            if byteVal is None:
                break
            if byteVal == ord('/'):
                nextByte = self.reader.readByte()
                if nextByte == ord('e'):
                    break
            byteArray.append(byteVal)
        return byteArray


def createFile(fileName):
    #Create the file path for extracted files from .tar file
    filePath = os.path.join(os.getcwd() + "/tar", fileName)
    #Check if the file path exists, if so, delete it then create it from the new one
    if os.path.isfile(filePath):
        os.remove(filePath)
        os.mknod(filePath)
    else:
        os.mknod(filePath)
    fd = os.open(filePath, os.O_RDWR)
    return fd

def encodeToFile(files):
    br = BufferedFdWriter(1)
    framer = Framer(br)

    for f in files:
        # Get the files from the /src directory 
        filePath = os.path.join(os.getcwd() + "/src", f)
        fileFd = os.open(filePath, os.O_RDONLY)

        # Initialize the reader
        fd = BufferedFdReader(fileFd)
        f = f.encode()
        framer.inputByteArray(f)
        framer.end()

        # Read through the files then write them to the buffer
        while ((byteVal := fd.readByte()) != None):
            framer.inputByte(byteVal)
        framer.end()

        fd.close()


def decodeFromFile(tarFile):
    # Initialize the reader
    tarPath = os.path.join(os.getcwd(), tarFile)
    tarFD = os.open(tarPath, os.O_RDONLY)
    tar = BufferedFdReader(tarFD)
    unframer = Unframer(tar)

    # Variable to tell if it's filename or content
    isName = 1
    fileName = ''

    # Read from the .tar file
    while ((byteVal := tar.readByte()) != None):
        # Check if the byte is the terminator for the framing
        check = unframer.checkByte(byteVal)
        # If terminator and filename
        if not check and isName:
            fd = createFile(fileName)
            out = BufferedFdWriter(fd)
            isName = 0
            fileName = ''
        # If terminator and not filename
        elif not check and not isName:
            out.close()
            isName = 1
        # If not a terminator and is filename
        elif check and isName:
            fileName += chr(byteVal)
        # If not a terminator and not filename
        elif check and not isName:
            out.writeByte(byteVal)
    print("\nFiles successfully decoded\n")
    tar.close()
            
        
        
# Create tar file
if usage == 'c':
    files = sys.argv[2:]
    encodeToFile(files)

# Extract from tar file to /tar directory
elif usage == 'x':
    tarFile = sys.argv[2]
    decodeFromFile(tarFile)

# Catch other issues to inform user
else:
    print("Invalid formatting.\n")
    print("Valid formatting is either: \n./mytar.py c <file1> <file2>...")
    print("Or:\n./mytar.py x <tarFile>")

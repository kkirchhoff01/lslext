import numpy
import math
import os
import sys
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt
from datetime import datetime

#Interpret input parameter
argument = sys.argv[1]

#Optional frame iteration limit
frameLimit = 0
if len(sys.argv)>2:
  frameLimit = sys.argv[2]

#Input file
file = open(argument,'rb')

# How many frames total?
file.seek(0, os.SEEK_END)
size = file.tell()
totalFrames = size/4128
#Go back to the beginning.
file.seek(-size,1)

#Is file size plausible?
#print "File size (bytes) is " + str(size) + ". This is " + str(totalFrames) + " frames."


#Don't iterate over everything if the user doesn't want to.
if frameLimit!=0:
  totalFrames = int(frameLimit)

#Create an IO stream. This will print 4096 lines per iteration. One line for each sample.
for i in xrange(totalFrames):
  frame = drx.readFrame(file)
  b1, t1, p1 = frame.parseID()
  for i in frame.data.iq.real[:]:
    print str(b1) + "," + str(t1) + "," +  str(frame.getCentralFreq()) + "," + str(p1) + "," + str(frame.data.iq.real[i]) + "," + str(frame.data.iq.imag[i])


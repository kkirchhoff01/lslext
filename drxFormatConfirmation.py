import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt
from datetime import datetime

file = open('/u/data/leap/observations/056777_000085151','rb')

frame1 = drx.readFrame(file)
frame2 = drx.readFrame(file)
frame3 = drx.readFrame(file)
frame4 = drx.readFrame(file)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "THIS IS HF ON MOON DATA"

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print "Tuning is: " + str(frame1.getCentralFreq())
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print "Tuning is: " + str(frame2.getCentralFreq())
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print "Tuning is: " + str(frame3.getCentralFreq())
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print "Tuning is: " + str(frame4.getCentralFreq())
print str(frame4.data.iq.real[:])


print "BEGIN NEXT FRAME SET FOR HF ON"

frame1 = drx.readFrame(file)
frame2 = drx.readFrame(file)
frame3 = drx.readFrame(file)
frame4 = drx.readFrame(file)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print "Tuning is: " + str(frame1.getCentralFreq())
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print "Tuning is: " + str(frame2.getCentralFreq())
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print "Tuning is: " + str(frame3.getCentralFreq())
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print "Tuning is: " + str(frame4.getCentralFreq())
print str(frame4.data.iq.real[:])

print "CHANGE TO HF OFF"

file1 = open('/u/data/leap/observations/056777_000085152','rb')


frame1 = drx.readFrame(file1)
frame2 = drx.readFrame(file1)
frame3 = drx.readFrame(file1)
frame4 = drx.readFrame(file1)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "THIS IS HF OFF MOON DATA"

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print "Tuning is: " + str(frame1.getCentralFreq())
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print "Tuning is: " + str(frame2.getCentralFreq())
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print "Tuning is: " + str(frame3.getCentralFreq())
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print "Tuning is: " + str(frame4.getCentralFreq())
print str(frame4.data.iq.real[:])


print "BEGIN NEXT FRAME SET FOR HF OFF"

frame1 = drx.readFrame(file)
frame2 = drx.readFrame(file)
frame3 = drx.readFrame(file)
frame4 = drx.readFrame(file)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print "Tuning is: " + str(frame1.getCentralFreq())
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print "Tuning is: " + str(frame2.getCentralFreq())
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print "Tuning is: " + str(frame3.getCentralFreq())
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print "Tuning is: " + str(frame4.getCentralFreq())
print str(frame4.data.iq.real[:])


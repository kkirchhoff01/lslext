import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt
from datetime import datetime

file = open('/u/data/leap/observations/056777_000085153','rb')

frame1 = drx.readFrame(file)
frame2 = drx.readFrame(file)
frame3 = drx.readFrame(file)
frame4 = drx.readFrame(file)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print str(frame4.data.iq.real[:])


print "BEGIN THE NEXT THINGY"

frame1 = drx.readFrame(file)
frame2 = drx.readFrame(file)
frame3 = drx.readFrame(file)
frame4 = drx.readFrame(file)

b1, t1, p1 = frame1.parseID()
b2, t2, p2 = frame2.parseID()
b3, t3, p3 = frame3.parseID()
b4, t4, p4 = frame4.parseID()

print "frame 1 stuff: " + str(b1) + ":" + str(t1) + ":" + str(p1)
print str(frame1.data.iq.real[:])
print "frame 2 stuff: " + str(b2) + ":" + str(t2) + ":" + str(p2)
print str(frame2.data.iq.real[:])
print "frame 3 stuff: " + str(b3) + ":" + str(t3) + ":" + str(p3)
print str(frame3.data.iq.real[:])
print "frame 4 stuff: " + str(b4) + ":" + str(t4) + ":" + str(p4)
print str(frame4.data.iq.real[:])

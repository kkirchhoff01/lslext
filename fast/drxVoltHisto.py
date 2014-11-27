import numpy
import sys
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt


framesToIterate =10
startAtFrame = 330000 

hf_on = open('/u/data/leap/observations/056777_000085153', 'rb')
hf_off = open('/u/data/leap/observations/056777_000085150', 'rb')
lf_on = open('/u/data/leap/observations/056777_000085151', 'rb')
lf_off = open('/u/data/leap/observations/056777_000085152', 'rb')

hf_on.seek((startAtFrame-1)*4128,0)
hf_off.seek((startAtFrame-1)*4128,0)
lf_on.seek((startAtFrame-1)*4128,0)
lf_off.seek((startAtFrame-1)*4128,0)

hf_onArr = []
hf_offArr = []
lf_onArr = []
lf_offArr = []
i = 0
while i<framesToIterate:
    i += 1
    hf_onTemp = drx.readFrame(hf_on)
    hf_onArr.extend(hf_onTemp.data.iq.real)
    hf_offTemp = drx.readFrame(hf_off)
    hf_offArr.extend(hf_offTemp.data.iq.real)
    lf_onTemp = drx.readFrame(lf_on)
    lf_onArr.extend(lf_onTemp.data.iq.real)
    lf_offTemp = drx.readFrame(lf_off)
    lf_offArr.extend(lf_offTemp.data.iq.real)


fig = plt.figure()
ax1 = fig.add_subplot(121)
hf_onx = plt.hist(hf_onArr[:],bins=8,histtype='step',normed=True,label = 'HF / On Moon')
hf_offx = plt.hist(hf_offArr[:],bins=8,histtype='step',normed=True,label = 'HF / Off Moon')
ax1.set_xlabel('Step')
ax1.set_ylabel('Count')
ax1.legend(loc='best')

ax2 = fig.add_subplot(122)
lf_onx = plt.hist(lf_onArr[:],bins=8,histtype='step',normed=True,label = 'LF / On Moon')
lf_offx = plt.hist(lf_offArr[:],bins=8,histtype='step',normed=True,label = 'LF / Off Moon')
ax2.set_xlabel('Step')
ax2.set_ylabel('Count')
ax2.legend(loc='best')

plt.show()

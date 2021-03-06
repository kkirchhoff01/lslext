from rmsIterator import rmsIterator
import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt

#chunks refers to number of DRX frames in an RMS calc, each frame ~209 microS
#a numpy array for 1 frame is 32,768 bytes. Fill CPU cache with frames for optimal performance. Saxon head node cache is 1024 KB.
#therefore 31.25 frames fit in the cache. Heavy lifting in thsi case is dot product of identical array, so assume ideal frame size of 15, with wiggle room built in.
chunks = 15
# how many chunks to plot
howManyChunks = (60*10)/0.003135
#fileArr is a list of four files, with the following order. HFON->HFOFF->LFON->LFOff
fileArr = [ '/u/data/leap/observations/056952_000117775', '/u/data/leap/observations/056952_000117776' ]


fig = plt.figure()
ax = fig.gca()
ax.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax.set_ylabel('ADC Magnitude')


hf_on = rmsIterator(fileArr[0],chunks)
hf_on.iterate(howManyChunks)

hf_off = rmsIterator(fileArr[1],chunks)
hf_off.iterate(howManyChunks)

#lf_on = rmsIterator(fileArr[2],chunks)
#lf_on.iterate(howManyChunks)

#lf_off = rmsIterator(fileArr[3],chunks)
#lf_off.iterate(howManyChunks)

ax.plot(hf_on.returnData[:],label='HF On')
ax.plot(hf_off.returnData[:],label='HF Off')
#ax.plot(lf_on.returnData[:],label='LF On')
#ax.plot(lf_off.returnData[:],label='LF Off')


ax.legend(loc='best')
fig.savefig('/u/home/qwofford/figures/rmsIteratorOutput/moonbounce1rms.png')

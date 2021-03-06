from rmsIterator import rmsIterator
import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt

#chunks refers to number of DRX frames in an RMS calc, each frame ~209 microS
chunks = 15
# how many chunks to plot
howManyChunks = 60*55/0.003135
#fileArr is a list of four files, with the following order. HFON->HFOFF->LFON->LFOff
fileArr = [ '/u/data/leap/observations/056885_000357550', '/u/data/leap/observations/056885_000357549', '/u/data/leap/observations/056885_000357552', '/u/data/leap/observations/056885_000357551' ]


fig = plt.figure()
ax = fig.gca()
ax.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax.set_ylabel('ADC Magnitude')


hf_on = rmsIterator(fileArr[0],chunks)
hf_on.iterate(howManyChunks)

hf_off = rmsIterator(fileArr[1],chunks)
hf_off.iterate(howManyChunks)

lf_on = rmsIterator(fileArr[2],chunks)
lf_on.iterate(howManyChunks)

lf_off = rmsIterator(fileArr[3],chunks)
lf_off.iterate(howManyChunks)

ax.plot(hf_on.returnData[:],label='HF On')
ax.plot(hf_off.returnData[:],label='HF Off')
ax.plot(lf_on.returnData[:],label='LF On')
ax.plot(lf_off.returnData[:],label='LF Off')


ax.legend(loc='best')
fig.savefig('/u/home/qwofford/figures/rmsIteratorOutput/08162014rms.png')

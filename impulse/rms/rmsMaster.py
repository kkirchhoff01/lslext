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
howManyChunks = 10 
#fileArr is a list of four files, with the following order. HFON->HFOFF->LFON->LFOff
fileArr = [ '/u/data/leap/observations/056777_000085153' ]


hf_on = rmsIterator(fileArr[0],chunks)
hf_on.iterate(howManyChunks)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax1.set_ylabel('ADC Magnitude')
ax2 = fig.add_subplot(222)
ax2.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax2.set_ylabel('ADC Magnitude')
ax3 = fig.add_subplot(223)
ax3.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax3.set_ylabel('ADC Magnitude')
ax4 = fig.add_subplot(224)
ax4.set_xlabel('Chunk # ('+str(0.000209*chunks)+' Seconds)')
ax4.set_ylabel('ADC Magnitude')


ax1.plot(hf_on.returnDataT1P0[:],label='B'+str(hf_on.beam)+'\:T'+str((hf_on.tune1/1e6))+'\:P0')
ax2.plot(hf_on.returnDataT1P1[:],label='B'+str(hf_on.beam)+'\:T'+str((hf_on.tune1/1e6))+'\:P1')
ax3.plot(hf_on.returnDataT2P0[:],label='B'+str(hf_on.beam)+'\:T'+str((hf_on.tune2/1e6))+'\:P0')
ax4.plot(hf_on.returnDataT2P1[:],label='B'+str(hf_on.beam)+'\:T'+str((hf_on.tune2/1e6))+'\:P1')


ax1.legend(loc='best')
ax2.legend(loc='best')
ax3.legend(loc='best')
ax4.legend(loc='best')
fig.savefig('/u/home/qwofford/figures/rmsIteratorOutput/rmsWIP.png')

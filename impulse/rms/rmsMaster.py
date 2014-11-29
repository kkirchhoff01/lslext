from rmsIterator import rmsIterator
import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt


class rmsMaster:
    def __init__(self, fileInput, fileOutput, framesPerChunk, howManyChunks):
        
        #chunks refers to number of DRX frames in an RMS calc, each frame ~209 microS
        #a numpy array for 1 frame is 32,768 bytes. Fill CPU cache with frames for optimal performance. Saxon head node cache is 1024 KB.
        #therefore 31.25 frames fit in the cache. Heavy lifting in thsi case is dot product of identical array, so assume ideal frame size of 15, with wiggle room built in.
        #chunks = 15
        self.framesPerChunk=framesPerChunk
        # how many chunks to plot
        self.howManyChunks= howManyChunks
        #fileArr is a list of four files, with the following order. HFON->HFOFF->LFON->LFOff
        self.fileInput = fileInput
        self.fileOutput = fileOutput

    def compute(self):
        self.rmsAnalysis = rmsIterator(self.fileInput,self.framesPerChunk)
        self.rmsAnalysis.iterate(self.howManyChunks)

        fig = plt.figure()

        ax1 = fig.add_subplot(221)
        ax1.set_xlabel('Chunk # ('+str(0.000209*self.framesPerChunk)+' Seconds)')
        ax1.set_ylabel('ADC Magnitude')
        ax2 = fig.add_subplot(222)
        ax2.set_xlabel('Chunk # ('+str(0.000209*self.framesPerChunk)+' Seconds)')
        ax2.set_ylabel('ADC Magnitude')
        ax3 = fig.add_subplot(223)
        ax3.set_xlabel('Chunk # ('+str(0.000209*self.framesPerChunk)+' Seconds)')
        ax3.set_ylabel('ADC Magnitude')
        ax4 = fig.add_subplot(224)
        ax4.set_xlabel('Chunk # ('+str(0.000209*self.framesPerChunk)+' Seconds)')
        ax4.set_ylabel('ADC Magnitude')


        ax1.plot(self.rmsAnalysis.returnDataT1P0[:],label='B'+str(self.rmsAnalysis.beam)+':T'+str("%.1f" % (self.rmsAnalysis.tune1/1e6))+':P0')
        ax2.plot(self.rmsAnalysis.returnDataT1P1[:],label='B'+str(self.rmsAnalysis.beam)+':T'+str("%.1f" % (self.rmsAnalysis.tune1/1e6))+':P1')
        ax3.plot(self.rmsAnalysis.returnDataT2P0[:],label='B'+str(self.rmsAnalysis.beam)+':T'+str("%.1f" % (self.rmsAnalysis.tune2/1e6))+':P0')
        ax4.plot(self.rmsAnalysis.returnDataT2P1[:],label='B'+str(self.rmsAnalysis.beam)+':T'+str("%.1f" % (self.rmsAnalysis.tune2/1e6))+':P1')


        ax1.legend(loc='best')
        ax2.legend(loc='best')
        ax3.legend(loc='best')
        ax4.legend(loc='best')

        fig.savefig(self.fileOutput)


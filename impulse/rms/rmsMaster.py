import sys
from rmsIterator import rmsIterator
import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import FormatStrFormatter

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
        print "I'm trying to compute."
        fig = plt.figure()  
        fig.set_size_inches(8,8)
        fig.subplots_adjust(hspace=0.25)

        ax1 = fig.add_subplot(221)
        ax1.set_xlabel('Time ('+str("%.6f" % (self.framesPerChunk*self.howManyChunks*4096/19.6e6))+' Seconds total)')
        ax1.set_ylabel('ADC Magnitude')
        ax2 = fig.add_subplot(222)
        ax2.set_xlabel('Time ('+str("%.6f" % (self.framesPerChunk*self.howManyChunks*4096/19.6e6))+' Seconds total)')
        ax2.set_ylabel('ADC Magnitude')
        ax3 = fig.add_subplot(223)
        ax3.set_xlabel('Time ('+str("%.6f" % (self.framesPerChunk*self.howManyChunks*4096/19.6e6))+' Seconds total)')
        ax3.set_ylabel('ADC Magnitude')
        ax4 = fig.add_subplot(224)
        ax4.set_xlabel('Time ('+str("%.6f" % (self.framesPerChunk*self.howManyChunks*4096/19.6e6))+' Seconds total)')
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

    def computeHist(self):
        self.rmsAnalysis = rmsIterator(self.fileInput,self.framesPerChunk)
        self.rmsAnalysis.iterate(self.howManyChunks)
        print "I'm trying to compute."
        fig = plt.figure()
        fig.set_size_inches(8,8)
        fig.subplots_adjust(hspace=0.25)

        ax1 = fig.add_subplot(221)
        fileAx1,bins1,trash1 = plt.hist(self.rmsAnalysis.returnDataT1P0[:],bins=8,histtype='step',normed=True,label = 'B'+str(self.rmsAnalysis.beam)+':T'+str("%.1f" % (self.rmsAnalysis.tune1/1e6))+":P0")
        ax1.set_xticks(bins1)
        ax1.xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        plt.setp(ax1.get_xticklabels(), rotation=90)
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Count')
        ax1.legend(loc='best')

        ax2 = fig.add_subplot(222)
        fileAx2,bins2,trash2 = plt.hist(self.rmsAnalysis.returnDataT1P1[:],bins=8,histtype='step',normed=True,label = "B"+str(self.rmsAnalysis.beam)+":T"+str("%.1f" % (self.rmsAnalysis.tune1/1e6))+":P1")
        ax2.set_xticks(bins2)
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        plt.setp(ax2.get_xticklabels(), rotation=90)
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Count')
        ax2.legend(loc='best')

        ax3 = fig.add_subplot(223)
        fileAx3,bins3,trash3 = plt.hist(self.rmsAnalysis.returnDataT2P0[:],bins=8,histtype='step',normed=True,label = "B"+str(self.rmsAnalysis.beam)+":T"+str("%.1f" % (self.rmsAnalysis.tune2/1e6))+":P0")
        ax3.set_xticks(bins3)
        ax3.xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        plt.setp(ax3.get_xticklabels(), rotation=90)
        ax3.set_xlabel('Step')
        ax3.set_ylabel('Count')
        ax3.legend(loc='best')

        ax4 = fig.add_subplot(224)
        fileAx4,bins4,trash4 = plt.hist(self.rmsAnalysis.returnDataT2P1[:],bins=8,histtype='step',normed=True,label = "B"+str(self.rmsAnalysis.beam)+":T"+str("%.1f" % (self.rmsAnalysis.tune2/1e6))+":P1")
        ax4.set_xticks(bins4)
        ax4.xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        plt.setp(ax4.get_xticklabels(), rotation=90)
        ax4.set_xlabel('Step')
        ax4.set_ylabel('Count')
        ax4.legend(loc='best')

        fig.savefig(self.fileOutput)

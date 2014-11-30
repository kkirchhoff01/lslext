import numpy
import sys
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt

class drxVoltHisto:
    def __init__(self,fileNameA, fileNameB):
        self.histoFileA = open(fileNameA, 'rb')
        self.histoFileB = open(fileNameB, 'rb')

    def compute(self, framesToIterate, startAtFrame):
        self.framesToIterate = 4*framesToIterate
        #Remember thre are four frames associated with a single sample in time, one for T1P0, T1P1, T2P0 and T2P1
        self.startAtFrame = 4*startAtFrame 
        try:
            self.histoFileA.seek((self.startAtFrame-1)*4128,0)
        except:
            print "Frame start bounds may be incorrect. Must start at frame >=1"
        self.histoArrT1P0A = []
        self.histoArrT1P1A = []
        self.histoArrT2P0A = []
        self.histoArrT2P1A = []
        try:
            self.histoFileB.seek((self.startAtFrame-1)*4128,0)
        except:
            print "Frame start bounds may be incorrect. Must start at frame >=1"
        self.histoArrT1P0B = []
        self.histoArrT1P1B = []
        self.histoArrT2P0B = []
        self.histoArrT2P1B = []
        self.beamA=-1
        self.beamB=-1
        self.tune1A=-1
        self.tune1B=-1
        self.tune2A=-1
        self.tune2B=-1
        i = 0
        while i<self.framesToIterate:
            i += 1
            self.histoT1P0TempA = drx.readFrame(self.histoFileA)
            self.histoArrT1P0A.extend(self.histoT1P0TempA.data.iq.real)
            self.histoT1P1TempA = drx.readFrame(self.histoFileA)
            self.histoArrT1P1A.extend(self.histoT1P1TempA.data.iq.real)
            self.histoT2P0TempA = drx.readFrame(self.histoFileA)
            self.histoArrT2P0A.extend(self.histoT2P0TempA.data.iq.real)
            self.histoT2P1TempA = drx.readFrame(self.histoFileA)
            self.histoArrT2P1A.extend(self.histoT2P1TempA.data.iq.real)
            self.histoT1P0TempB = drx.readFrame(self.histoFileB)
            self.histoArrT1P0B.extend(self.histoT1P0TempB.data.iq.real)
            self.histoT1P1TempB = drx.readFrame(self.histoFileB)
            self.histoArrT1P1B.extend(self.histoT1P1TempB.data.iq.real)
            self.histoT2P0TempB = drx.readFrame(self.histoFileB)
            self.histoArrT2P0B.extend(self.histoT2P0TempB.data.iq.real)
            self.histoT2P1TempB = drx.readFrame(self.histoFileB)
            self.histoArrT2P1B.extend(self.histoT2P1TempB.data.iq.real)
            self.tune1A = (self.histoT1P0TempA.getCentralFreq()/1e6)
            self.tune2A = (self.histoT2P0TempA.getCentralFreq()/1e6)
            self.tune1B = (self.histoT1P0TempB.getCentralFreq()/1e6)
            self.tune2B = (self.histoT2P0TempB.getCentralFreq()/1e6)
            self.beamA, self.dontCare, self.irrelevant = self.histoT1P0TempA.parseID()
            self.beamB, self.dontCare, self.irrelevant = self.histoT1P0TempB.parseID()
        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        fileAx1 = plt.hist(self.histoArrT1P0A[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamA)+":T"+str("%.1f" % self.tune1A)+":P0")
        fileBx1 = plt.hist(self.histoArrT1P0B[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamB)+":T"+str("%.1f" % self.tune1B)+":P0")
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Count')
        ax1.legend(loc='best')

        ax2 = fig.add_subplot(222)
        fileAx2 = plt.hist(self.histoArrT1P1A[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamA)+":T"+str("%.1f" % self.tune1A)+":P1")
        fileBx2 = plt.hist(self.histoArrT1P1B[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamB)+":T"+str("%.1f" % self.tune1A)+":P1")
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Count')
        ax2.legend(loc='best')

        ax3 = fig.add_subplot(223)
        fileAx3 = plt.hist(self.histoArrT2P0A[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamA)+":T"+str("%.1f" % self.tune2A)+":P0")
        fileBx3 = plt.hist(self.histoArrT2P0B[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamB)+":T"+str("%.1f" % self.tune2A)+":P0")
        ax3.set_xlabel('Step')
        ax3.set_ylabel('Count')
        ax3.legend(loc='best')

        ax4 = fig.add_subplot(224)
        fileAx4 = plt.hist(self.histoArrT2P1A[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamA)+":T"+str("%.1f" % self.tune2A)+":P1")
        fileBx4 = plt.hist(self.histoArrT2P1B[:],bins=8,histtype='step',normed=True,label = "B"+str(self.beamB)+":T"+str("%.1f" % self.tune2A)+":P1")
        ax4.set_xlabel('Step')
        ax4.set_ylabel('Count')
        ax4.legend(loc='best')

        plt.show()

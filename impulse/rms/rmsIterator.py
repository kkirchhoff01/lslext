import sys
import numpy
import math
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB
from matplotlib import pyplot as plt
from datetime import datetime

#04302014run.txt  05022014run.txt  07172014run.txt  filelist.txt            MoonBounce2run.txt
#05012014run.txt  06182014run.txt  08162014run.txt  MoonBounce1run.txt

class rmsIterator:
    def __init__(self,file,chunkSizeinFrames):
        #(NEXT STEP) Implement class def with these variables as parameters
        self.beam=-123
        self.returnDataT1P0=[]
        self.returnDataT1P1=[]
        self.tune1=-123
        self.returnDataT2P0=[]
        self.returnDataT2P1=[]
        self.tune2=-123
        self.chunkArrayT1P0=[]
        self.chunkArrayT1P1=[]
        self.chunkArrayT2P0=[]
        self.chunkArrayT2P1=[]
        self.chunkSizeinFrames=chunkSizeinFrames
        self.file=file
        self.input = open(self.file, 'r')
        self.timer = datetime.now()
        #END NEXT STEP

    def simpleRMS(self):
        self.timer = datetime.now()
        #Note: Every time readframe is used, the open file is incremented by the frame size
        i = 0
        self.chunkArrayT1P0=[]
        self.chunkArrayT1P1=[]
        self.chunkArrayT2P0=[]
        self.chunkArrayT2P1=[]
        #Make sure analysis starts with T1P0
        self.tmpFrame = drx.readFrame(self.input)
        self.beamTmp, self.tuneTmp, self.polTmp = self.tmpFrame.parseID()
        while self.tuneTmp != 1 & self.polTmp != 0:
            print "T" + str(self.tuneTmp) + ":P" + str(self.polTmp) + " isn't a good place to start."
            self.tmpFrame = drx.readFrame(self.input)
            self.beamTmp, self.tuneTmp, self.polTmp = self.tmpFrame.parseID()
            print "Seeking to T" + str(self.tuneTmp) + ":P" + str(self.polTmp)
        #Found it! Go back one frame and start analysis
        #print "Beginning with Tuning " + str(self.tuneTmp) + " @ " + str(self.tmpFrame.getCentralFreq()) + "MHz. Polarity " + str(self.polTmp) +".\n" 
        self.input.seek(-4128,1)
        
        while i <= self.chunkSizeinFrames:
            #T1P0 read
            self.thisFrame = drx.readFrame(self.input)
            #T1P1 read
            self.thatFrame = drx.readFrame(self.input)
            #T2P0 read
            self.anotherFrame = drx.readFrame(self.input)
            #T2P1 read
            self.theOtherFrame = drx.readFrame(self.input)
            #Store the relevent data
            self.chunkArrayT1P0.extend(self.thisFrame.data.iq.real[:])
            #print "Current T1P0 timestamp: " + str("%.9f" % self.thisFrame.getTime())
            self.chunkArrayT1P1.extend(self.thatFrame.data.iq.real[:])
            #print "Current T1P1 timestamp: " + str("%.9f" % self.thatFrame.getTime())
            self.chunkArrayT2P0.extend(self.anotherFrame.data.iq.real[:])
            #print "Current T2P0 timestamp: " + str("%.9f" % self.anotherFrame.getTime())
            self.chunkArrayT2P1.extend(self.theOtherFrame.data.iq.real[:])
            #print "Current T2P1 timestamp: " + str("%.9f" % self.theOtherFrame.getTime())
            i += 1
        #Store header info for labeling plots
        self.beam, self.dontCare, self.irrelevant= self.thisFrame.parseID()
        self.tune1=self.thisFrame.getCentralFreq()
        self.tune2=self.anotherFrame.getCentralFreq()
        #print 'Processing this many frames as a chunk: ' + str(-1+len(self.chunkArrayT1P0)/4096)
        numpyArrT1P0 = numpy.array(self.chunkArrayT1P0)
        numpyArrT1P1 = numpy.array(self.chunkArrayT1P1)
        numpyArrT2P0 = numpy.array(self.chunkArrayT2P0)
        numpyArrT2P1 = numpy.array(self.chunkArrayT2P1)
        #Store RMS for chunk in the relevant returnDataXXYY format
        self.returnDataT1P0.append(math.sqrt(numpy.dot(numpyArrT1P0,numpyArrT1P0)/(self.chunkSizeinFrames*4096)))
        self.returnDataT1P1.append(math.sqrt(numpy.dot(numpyArrT1P1,numpyArrT1P1)/(self.chunkSizeinFrames*4096)))
        self.returnDataT2P0.append(math.sqrt(numpy.dot(numpyArrT2P0,numpyArrT2P0)/(self.chunkSizeinFrames*4096)))
        self.returnDataT2P1.append(math.sqrt(numpy.dot(numpyArrT2P1,numpyArrT2P1)/(self.chunkSizeinFrames*4096)))
        #print 'Chunk block (T1P0 and T1P1 and T2P0 and T2P1) processing time: ' + str(datetime.now()-self.timer)
    def iterate(self, numberChunks):
        self.totalTime = datetime.now()
        j = 0
        while (j < numberChunks):
            if ( (j+1)%50 == 0 ):
                print 'Working on chunk #' + str(1+(j))
            self.simpleRMS()
            j += 1
        #Clean up working array
        self.chunkArray=[]
        print 'TOTAL iteration time for file: ' + str(datetime.now()-self.totalTime)

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
        self.returnData=[]
        self.chunkArray=[]
        self.chunkSizeinFrames=chunkSizeinFrames
        self.file=file
        self.input = open(self.file, 'r')
        self.timer = datetime.now()
        #END NEXT STEP

    def simpleRMS(self):
        self.timer = datetime.now()
        #Note: Every time readframe is used, the open file is incremented by the frame size
        i = 0
        self.chunkArray=[]
        while i <= self.chunkSizeinFrames:
            self.thisFrame = drx.readFrame(self.input)
            self.chunkArray.extend(self.thisFrame.data.iq.real[:])
            i += 1
#        print 'Processing this many frames as a chunk: ' + str(-1+len(self.chunkArray)/4096)
        numpyArr = numpy.array(self.chunkArray)
#        print numpyArr
        self.returnData.append(math.sqrt(numpy.dot(numpyArr,numpyArr)/(self.chunkSizeinFrames*4096)))
#        print 'Chunk processing time: ' + str(datetime.now()-self.timer)
    def iterate(self, numberChunks):
        self.totalTime = datetime.now()
        j = 0
        while (j < numberChunks):
#            print 'Working on chunk #' + str(1+(j))
            self.simpleRMS()
            j += 1
        #Clean up working array
        self.chunkArray=[]
        print 'TOTAL iteration time for file: ' + str(datetime.now()-self.totalTime)

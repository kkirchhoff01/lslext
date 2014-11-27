import numpy
import sys
from datetime import datetime
from scipy import signal
from lsl.reader import drx
from lsl.correlator import fx as fxc
from lsl.misc.mathutil import to_dB

class templateCorrelation:
	def __init__(self,file,startFrame):
		#Variable declaration
		self.startFrame = int(startFrame)
		self.file = file
		self.fh = open(file, 'r')
		self.realTune1 = []
		self.imagTune1 = []
		self.realTune2 = []
		self.imagTune2 = []
		self.template = self.getTemplate()
	#End __init__
	
	def getTemplate(self):
		temp = []
		#get template data
		t = open('a3.txt','r')
		for line in t:
			temp.append(float(line)/40)
		t.close()
		return temp
	#End getTemplate
		
	#iterate through frames in xrange
	def correlateData(self,frameLimit):
		sample = []
		self.fh.seek((self.startFrame)*4128,0)
		steps = frameLimit/10
		totalTime = datetime.now()
		print 'Correlating [          ]',
		print '\b'*12,
		sys.stdout.flush()
		for p in xrange(frameLimit):
			startTime = datetime.now()
			frame = drx.readFrame(self.fh)		
			
			if frame.parseID()[1] == 1:
				self.realTune1 = self.realTune1 + numpy.correlate(frame.data.iq.real,self.template).tolist()
				self.imagTune1 = self.imagTune1 + numpy.correlate(frame.data.iq.imag,self.template).tolist()
			else:
				self.realTune2 = self.realTune2 + numpy.correlate(frame.data.iq.real,self.template).tolist()
				self.imagTune2 = self.imagTune2 + numpy.correlate(frame.data.iq.imag,self.template).tolist()
			if p%steps == 0:
				print '\b=',
				sys.stdout.flush()
		print '\b] Done'
		self.startFrame += frameLimit	
		#self.fh.close()
		print 'Read time: ' + str(datetime.now() - totalTime)

	def resetData(self):
		self.realTune1 = []
		self.imagTune1 = []
		self.realTune2 = []
		self.imagTune2 = []

	def closeFile(self):
		self.fh.close()

import numpy as np
import sys
from matplotlib import pyplot as plt
from datetime import datetime
from lsl.reader import drx, errors
import h5py 

'''
To run the script:
	python topCorrelations.py <file location> <number of frames>
Number of frames is optional. If left out, the program will iterate over the entire file.

a3.txt (the template file) must be in the same folder as this script.
'''

#File and frame number variables
file = ''
numFrames = sys.maxint

if len(sys.argv) == 2:
	file = str(sys.argv[1])
	print 'Using ' + file + ' for all frames.\n'
elif len(sys.argv) == 3:
	file = str(sys.argv[1])
	numFrames = int(sys.argv[2])
	print 'Using ' + file + ' with ' + str(numFrames) + ' frames.\n'
else:
	print 'Invalid arguments.'
	exit()
#Read template
temp = np.fromfile(file='a3.txt', dtype = float, sep='\n')
for t in temp:
	t = t/40.0

#Variable declaration
realdata = np.array((100,100), dtype=float)#[(0,0)] * 100
imagdata = np.array((100,100), dtype=float)#[(0,0)] * 100
realmincorr = 0.0
imagmincorr = 0.0
fh = open(file, 'r');
startTime = datetime.now()

#Main file loop
for i in xrange(numFrames):
	#File reading/eof catching
	try:
		frame = drx.readFrame(fh)
	except errors.eofError:
		errorfile = open('/u/home/kkirchhoff/Top_Correlations_HDF/' + file[:26] + '.log', 'w')
		errorfile.write('File ended at ' + str(datetime.now()) + ' on frame ' + str(i))
		errorfile.close()
		break

	#Count sample vairalbes
	realcount = 0
	imagcount = 0
	#Correlations
	realcorr = np.correlate(frame.data.iq.real,temp,'same')
	imagcorr = np.correlate(frame.data.iq.imag,temp,'same')
	#Maximum correlation loops
	'''
	#This is horrible. Why did I do this?
	for j in realcorr:
		if abs(j) > realmincorr:
			realdata.append((j,(i*4096)+realcount))
			realdata.sort(key= lambda corrsize: abs(corrsize[0]), reverse=True)
			realdata.pop()
			realmincorr = abs(realdata[len(realdata)-1][0])
		realcount += 1
	for k in imagcorr:
		if abs(k) > imagmincorr:
			imagdata.append((k,(i*4096)+imagcount))
			imagdata.sort(key= lambda corrsize: abs(corrsize[0]), reverse=True)
			imagdata.pop()
			imagmincorr = abs(imagdata[len(imagdata)-1][0])
		imagcount += 1
	'''
fh.close()
endtime = str(datetime.now() - startTime)
#Write the run time to log file
logfile = open('/u/home/kkirchhoff/Top_Correlations_HDF/' + file[:26] + '.log', 'w')
logfile.write('Total run time: ' + endtime)
logfile.close()
#Write the correlations to an hdf5 file
fname = '/u/home/kkirchhoff/Top_Correlations_HDF/top_correlations_'+file[26:]+'.hdf5'
f = h5py.File(fname,'w')#'top_corretations_' + file' +'.hdf5','w')
f.create_dataset("real_dataset",data=realdata)
f.create_dataset("imag_dataset",data=imagdata)
f.close()

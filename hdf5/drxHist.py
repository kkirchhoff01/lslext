import numpy as np
import sys
from datetime import datetime
from lsl.reader import drx, errors
import h5py
from matplotlib import pyplot as plt

file = ''
numFrames = 10000

if len(sys.argv) == 2:
	file = str(sys.argv[1])
	print 'Using ' + file + ' with ' + str(numFrames) + ' frames.\n'
elif len(sys.argv) == 3:
	file = str(sys.argv[1])
	numFrames = int(sys.argv[2])
	print 'Using ' + file + ' with ' + str(numFrames) + ' frames.\n'
else:
	print 'Invalid arguments.'
	exit()

temp = []
t = open('a3.txt','r')
for line in t:
	temp.append(float(line)/40)
t.close()
maxbin = 0
minbin = 0

fname = '/u/home/kkirchhoff/Top_Correlations_HDF/top_correlations_'+file[26:]+'.hdf5'
f = h5py.File(fname,'r')
ds = f['dataset_1'][:]
f.close()
ds = ds.tolist()[:]
maxbin = max(ds)[0]
minbin = min(ds)[0]

fh = open(file, 'r');
histdata = np.zeros(50,dtype='int32')

startTime = datetime.now()
print 'Correlating [                         ]',
print '\b'*27,
sys.stdout.flush()
for i in xrange(numFrames):
	try:
		frame = drx.readFrame(fh)
	except errors.baseReaderError().eofError:
		errorfile = open('/u/home/kkirchhoff/Top_Correlations_HDF/errors.log', 'w')
		errorfile.write('File ended at ' + str(datetime.now()) + ' on frame ' + str(i))
		errorfile.close()
		break

	corr = np.correlate(frame.data.iq.real,temp,'same')
	hist, edges = np.histogram(corr,bins=50,range=(minbin,maxbin))
	histdata += hist
	if i%(numFrames/25)  == 0:
		print '\b=',
		sys.stdout.flush()

print '\b] Done'
print 'Total time: '+str(datetime.now() - startTime)
fh.close()
print histdata
fig = plt.figure(figsize=(12,9), dpi=100)
#n, bins, patches = plt.hist(histdata,bins=50, histtype='bar',align='mid')
plt.bar(np.arange(50),histdata)
plt.xticks(np.arange(50), np.arange(minbin,maxbin, dtype='int32'), size=8)
plt.title('Correlations for ' + file[26:])
plt.ylabel('Correlation Count')
plt.xlabel('Correlation Value')
#plt.show()
fig.savefig('/u/home/kkirchhoff/Top_Correlations_HDF/Histograms/correlation_hist' + file[26:])

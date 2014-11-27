from templateCorrelation import templateCorrelation
from datetime import datetime
from matplotlib import pyplot as plt

plt.rcParams['agg.path.chunksize'] = 50000
fig = plt.figure()
#ax = fig.gca()

ax1 = fig.add_subplot(211)
ax1.set_xlabel('Samples')
ax1.set_ylabel('Tuning 1 Correlation')

ax2 = fig.add_subplot(212)
ax2.set_xlabel('Samples')
ax2.set_ylabel('Tuning 2 Correlation')

file = '/u/data/leap/observations/056952_000117775'
frames = 250
atFrame = 861000
startTime = datetime.now()

rt1 = []
it1 = []
rt2 = []
it2 = []

framesAt = []

tc = templateCorrelation(file,atFrame)
for i in xrange(2):
	tc.correlateData(frames)
	rt1 += tc.realTune1
	it1 += tc.imagTune1
	rt2 += tc.realTune2
	it2 += tc.imagTune2
	tc.resetData()

print 'Total time: '+str(datetime.now() - startTime)
tc.closeFile()

#Seperated correlation plotting
ax1.plot(rt1, label="Real Data")
ax1.plot(it1, label='Imaginary Data')
#ax1.legend(loc=0)
ax1.set_xlim([0,len(rt1)])

ax2.plot(rt2, label='Real Data')
ax2.plot(it2, label='Imaginary Data')
#ax2.legend(loc=0)
ax2.set_xlim([0,len(rt2)])

print 'Plotting.'
#fig.savefig('/u/home/kkirchhoff/CorrelationPlots/correlation'+str(datetime.now())+'.png')
#ax2.set_ylim([-3,3])
plt.show()

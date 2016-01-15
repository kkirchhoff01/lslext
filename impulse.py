import numpy as np
from matplotlib import pyplot as plt

path = ''#'/Users/kevinkirchhoff/Documents/Programming/Python/Impulse_Measurements/'
#List of file names to iterate over
fnames = [path + 'fat_swr.csv', path + 'lwa111.csv', path + 'scope_9.csv']

fatswr = []
lwaswr = []
scopedata = []

count = 0
#Parsing code
#Iterates through each file name
for f in fnames:
	temp = []
	#Takes the file name, opens it and reads in the lines
	with open(f, 'r') as rf:
		temp = temp + rf.readlines()
	#Parses the first file
	if count == 0:
		for i in temp[18:]:
			t = [x.strip('"\n\r') for x in i.split(',')]
			fatswr.append((float(t[0]),float(t[1])))
		count += 1
	#Parses the second file
	elif count == 1:
		for i in temp[18:]:
			t = [x.strip('"\n\r') for x in i.split(',')]
			lwaswr.append((float(t[0]),float(t[1])))
		count += 1
	#Parses the third file
	else:
		for i in temp[2:]:
			t = [x.strip('+\n').split('E') for x in i.split(',')][:]
			a = float(t[0][0])*(10**float(t[0][1]))
			b = float(t[1][0])*(10**float(t[1][1]))
			c = float(t[2][0])*(10**float(t[2][1]))
			scopedata.append((a,b,c))
	
#Calculate fft from scope data
fftdata1 = np.fft.fft([x[1] for x in scopedata])
fftdata2 = np.fft.fft([x[2] for x in scopedata])

#Power ratio
ratio = sum([np.linalg.norm(x) for x in fftdata1[0:500]])/sum([np.linalg.norm(x) for x in fftdata1[60:80]])
print ratio
print 1/ratio

freqdata1 = []
freqdata2 = []
#Bins the fft data into two second intervals and multiplies it by the swr data
for n in range(len(scopedata)/2):
	if n < 30 or n > ((len(scopedata)/2)-30):
		b1 = 0
		b2 = 0
	else:
		b1 = (fftdata1[2*n]+fftdata1[2*n+1])/2
		b2 = (fftdata2[2*n]+fftdata2[2*n+1])/2
	freqdata1.append(b1*fatswr[n][1]*lwaswr[n][1])
	freqdata2.append(b2*fatswr[n][1]*lwaswr[n][1])

#Takes the ifft of V(f) multiplied by the swr data
ifftdata1 = np.fft.ifft(freqdata1)
ifftdata2 = np.fft.ifft(freqdata2)

#Plotting
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
ax1.plot(ifftdata1)
ax1.set_title('LWA Data')
ax2.plot(ifftdata2)
ax2.set_title('Direct Scope Data')
plt.xlabel('Frequency Interval Number')
ax1.set_ylabel('FFT Output')
ax2.set_ylabel('FFT Output')
plt.show()

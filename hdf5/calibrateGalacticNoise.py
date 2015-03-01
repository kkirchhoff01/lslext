#!/usr/bin/pyth
import matplotlib.pyplot as pyp
import h5py
import cmath
import numpy.fft
import numpy

def getDoubleSidedFFT(freq, ft):
	df = freq[1]-freq[0]
	n = len(ft)
	bfreq = numpy.arange(-1*freq[-1], freq[-1], df)
	bft = sqrt(2.)*numpy.zeros(len(bfreq), dtype=complex)
	bft[-1-n:-1] = ft                   #positive frequencies
	bft[0:n] = ft[::-1]                 #negative frequencies
	return bfreq, bft

fname = '056726_000355307-waterfall-complex`.hdf5'
f = h5py.File(fname, 'r')

freq = f['Observation1']['Tuning1']['freq']
mod = f['Observation1']['Tuning1']['XXmag'][0]
phase = f['Observation1']['Tuning1']['XXphase'][0]

pyp.figure(2)
pyp.plot( freq, phase, label='phase')
pyp.ylabel('FFT phase angle (radians)')
pyp.xlabel('Frequency (Hz)')

pyp.figure(1)
pyp.plot( freq, mod, label='magnitude')
pyp.xlabel("Frequency (Hz)")
pyp.ylabel("FFT magnitude (ADC/Hz)")
#pyp.legend()

pyp.figure(3)
pyp.plot(freq, 10*numpy.log10(mod*mod), label='PSD')
pyp.xlabel('Frequency (MHz)')
pyp.ylabel('Power Spectral Density (dB/Hz)')

pyp.figure(1)
ft = mod*numpy.cos(phase) + 1j*mod*numpy.sin(phase) 
pyp.plot( freq, abs(ft), label='complex')

# error checking & filtering
for i,f in enumerate(ft):
	if( f!=f ):  # checks for NaN's which break the ifft
		ft[i] = ft[i-1]

samprate = 19.6e6 #digitizing at 19.6 MSPS 
wv = numpy.fft.ifft(numpy.fft.ifftshift(ft))
tm = numpy.arange(len(wv))*1./samprate*1e6 # in micro-seconds 
off = numpy.nanmax(abs(wv))
print wv
print off
pyp.figure(4)
pyp.plot(tm, wv+off, label='original')

# error checking & filtering
filters = [[88.2473e6, 88.3501e6], [89.0253e6, 89.1639e6]]
for i,f in enumerate(ft):
	if( f!=f ):  # checks for NaN's which break the ifft
		ft[i] = ft[i-1]
	for fil in filters:
		if (freq[i] > fil[0] and freq[i] < fil[1]):
			ft[i] = 0.

pyp.figure(1)
pyp.plot( freq, abs(ft), label='filtered')
pyp.legend(loc='upper left')

wv = numpy.fft.ifft(numpy.fft.ifftshift(ft))

pyp.figure(4)
pyp.plot(tm, wv-off, label='filtered')
pyp.xlabel('Time ($\mu s$)')
pyp.ylabel('ADC counts')
pyp.legend(loc='upper left')

pyp.show()

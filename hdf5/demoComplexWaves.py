#!/usr/bin/python
import matplotlib.pyplot as pyp
import h5py
import cmath
import numpy.fft
import numpy
import pandas as pd
import scipy.optimize as optimization

def rayleigh_func(x, sigma):
	return x*numpy.exp(-pow(x/sigma, 2))/pow(sigma,2)

def getDoubleSidedFFT(freq, ft):
	df = freq[1]-freq[0]
	n = len(ft)
	bfreq = numpy.arange(-1*freq[-1], freq[-1], df)
	bft = numpy.zeros(len(bfreq), dtype=complex)
	bft[-1-n:-1] = ft                   #positive frequencies
	bft[0:n] = ft[::-1]                 #negative frequencies
	return bfreq, bft

#fname = '/u/data/leap/hdf/056855_000082430-waterfall-complex.hdf5'
fname = '/u/data/leap//rfi/hdf_filt/056777_000085150-0-waterfall-complex.hdf5'
drxfile = h5py.File(fname, 'r')
# the data are organized by observation (one per file), tuning (two per file).
# each tuning has a freq, (Xmag, Xphase)->magnitude and phase of complex fft
# there are two ffts per tuning, corresponding to the two linear polarizaitons.
#
# To explote the HDF5 file, open an interactive python shell (ipython on the commandline)
# fname = '/u/data/leap/hdf/056726_000355307-waterfall.hdf5' 
# import h5py
# f = h5py.File(fname, 'r')
# print f.keys()
# print f['Observation'].keys() --> contains the timing information for a given specturm in "time"
# print f['Observation']['Tuning1'].keys() --> contains the complex fft for both polarizations, XX & YY
# 
# There are nChunk ffts in a given tuning and polarization, corresponding to the total time in the file divided by the time overwhich the spectra are averaged. For example, spectra averaged over 0.1s for 1 s gives 10 chunks. 
for ichunk in range(4):
	print ichunk, drxfile.keys() 
	freq = drxfile['Observation1']['Tuning1']['freq']
	mod = drxfile['Observation1']['Tuning1']['XXmag'][ichunk]
	phase = drxfile['Observation1']['Tuning1']['XXphase'][ichunk]

	pyp.figure(2)
	pyp.subplot(2,2,ichunk+1)
	pyp.plot( freq, phase, label='phase' + str(ichunk))
	pyp.ylabel('FFT phase angle (radians)')
	pyp.xlabel('Frequency (Hz)')

	pyp.figure(1)
	pyp.subplot(2,2,ichunk+1)
	pyp.plot( freq, abs(mod)/19.6e6, label='magnitude' + str(ichunk))
	pyp.xlabel("Frequency (Hz)")
	pyp.ylabel("FFT magnitude (ADC/Hz)")
	#pyp.legend()

	pyp.figure(3)
	pyp.subplot(2,2,ichunk+1)
	pyp.plot(freq, 10*numpy.log10(pow(abs(mod), 2) )/19.6e6, label='PSD' + str(ichunk))
	pyp.xlabel('Frequency (MHz)')
	pyp.ylabel('Power Spectral Density (dB/Hz)')

	pyp.figure(1)
	pyp.subplot(2,2,ichunk+1)
	ft = mod*numpy.cos(phase) + 1j*mod*numpy.sin(phase) 
	pyp.plot( freq, abs(ft)/19.6e6, label='complex' + str(ichunk))

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
	filters = [[7.1076e7,7.10827e7], [7.23894e7, 7.24036e7]]
	for i,f in enumerate(ft):
		if( f!=f ):  # checks for NaN's which break the ifft
			ft[i] = ft[i-1]
		for fil in filters:
			if (freq[i] > fil[0] and freq[i] < fil[1]):
				ft[i] = 0.

	pyp.figure(1)
	pyp.subplot(2,2,ichunk+1)
	pyp.plot( freq, abs(ft)/19.6e6, label='filtered' + str(ichunk))
	pyp.legend(loc='lower right')

	wv = numpy.fft.ifft(numpy.fft.ifftshift(ft))

	pyp.figure(4)
	pyp.subplot(2,2,ichunk+1)
	pyp.plot(tm, wv-off, label='filtered' + str(ichunk))
	pyp.xlabel('Time ($\mu s$)')
	pyp.ylabel('ADC counts')
	pyp.legend(loc='upper left')


	pyp.figure(5)
	pyp.subplot(2,2,ichunk+1)
	famp = pd.Series(mod).dropna()
	n,bins,patches = pyp.hist(famp, 30, normed=1, histtype='step')
	pyp.clf()
	#pyp.plot(bins[:-1], n)
	x0 = [numpy.std(famp)]
	print n, bins, patches
	popt,pcov= optimization.curve_fit(rayleigh_func,bins[:-1],n/sum(n),x0)
	print popt
	print pcov
	pyp.plot( bins[:-1], rayleigh_func(bins[:-1], popt[0]), label=str(popt[0]))
	pyp.legend()
	pyp.xlabel('Fourier Amplitudes')

pyp.show()

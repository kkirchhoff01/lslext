#!/usr/bin/python
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as pyp
import h5py
import cmath
import numpy.fft
import numpy
import pandas as pd
import scipy.optimize as optimization
import sys
import re

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

fname = sys.argv[1]
ffname = sys.argv[2]
#fname = '/u/data/leap/hdf/056855_000082430-waterfall-complex.hdf5'
#fname = '/u/data/leap/hdf/056777_000085150-0-waterfall-complex.hdf5'
drxfile = h5py.File(fname, 'r')
fildrxfile = h5py.File(ffname, 'r')

m = re.search("(\d+_\d+)", fname)
fnumber = m.group(0)
m = re.search("-(\d+)-", fname)
fsec = m.group(1)

# the data are organized by observation (one per file), tuning (two per file).
# each tuning has a freq, (Xmag, Xphase)->magnitude and phase of complex fft
# there are two ffts per tuning, corresponding to the two linear polarizaitons.
#
# To explore the HDF5 file, open an interactive python shell (ipython on the commandline)
# fname = '/u/data/leap/hdf/056726_000355307-waterfall.hdf5' 
# import h5py
# f = h5py.File(fname, 'r')
# print f.keys()
# print f['Observation'].keys() --> contains the timing information for a given specturm in "time"
# print f['Observation']['Tuning1'].keys() --> contains the complex fft for both polarizations, XX & YY
# 
# There are nChunk ffts in a given tuning and polarization, corresponding to the total time in the file divided by the time overwhich the spectra are averaged. For example, spectra averaged over 0.1s for 1 s gives 10 chunks. Averaging over 208microseconcds for 1s gives 4807 chunks. 

# set up output files
outdir = '/u/data/leap/noise/'
fname_wfm = outdir + fnumber + '-'+fsec  + '_wfm.dat'
fwfm = open(fname_wfm, 'w') 
fname_fd = outdir + fnumber + '-'+fsec +'_fd.dat'
ffd = open(fname_fd, 'w')

nchunks = len(drxfile['Observation1']['Tuning1']['XXmag'])

for ichunk in range(nchunks):
	#print ichunk, drxfile.keys() 
	if ichunk % 100 == 0:
		print "Processing frame ", ichunk, "/",nchunks
	for itune, tune in enumerate(['Tuning1','Tuning2']):
		for ipol, pol in enumerate(['XX','YY']):
			#print tune, pol+'mag', ichunk
			freq = drxfile['Observation1'][tune]['freq']
			mod = drxfile['Observation1'][tune][pol+'mag'][ichunk]
			phase = drxfile['Observation1'][tune][pol+'phase'][ichunk]

			ffreq = fildrxfile['Observation1'][tune]['freq']
			fmod = fildrxfile['Observation1'][tune][pol+'mag'][ichunk]
			fphase = fildrxfile['Observation1'][tune][pol+'phase'][ichunk]

			# error checking & filtering
			ft = mod*numpy.cos(fphase) + 1j*mod*numpy.sin(fphase) 
			for i,f in enumerate(ft):
				if( f!=f ):  # checks for NaN's which break the ifft
					ft[i] = ft[i-1]

			samprate = 19.6e6 #digitizing at 19.6 MSPS 
			if( min(freq) < 0.):
				print "This is a full spectrum, not a real one"
			wv = numpy.fft.irfft(ft)
			tm = numpy.arange(len(wv))*1./samprate*1e6 # in micro-seconds 
			off = numpy.nanmax(abs(wv))

			# next plot the filtered stuff
			# error checking & filtering
			fft = fmod*numpy.cos(fphase) + 1j*fmod*numpy.sin(fphase) 
			for i,f in enumerate(fft):
				if( f!=f ):  # checks for NaN's which break the ifft
					fft[i] = fft[i-1]

			samprate = 19.6e6 #digitizing at 19.6 MSPS 
			fwv = numpy.fft.irfft(fft)
			tm = numpy.arange(len(fwv))*1./samprate*1e6 # in micro-seconds 
			off = numpy.nanmax(abs(fwv))

			if( ichunk < 4): # plot only the first four frames
				# first plot the original waveform
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

				pyp.figure(4)
				pyp.subplot(2,2,ichunk+1)
				pyp.plot(tm, wv+off, label='original')
				pyp.legend(loc='upper left')

				pyp.figure(1)
				pyp.subplot(2,2,ichunk+1)
				pyp.plot( ffreq, abs(fft)/19.6e6, label='filtered' + str(ichunk))
				pyp.legend(loc='lower right')

				pyp.figure(4)
				pyp.subplot(2,2,ichunk+1)
				pyp.plot(tm, fwv-off, label='filtered' + str(ichunk))
				pyp.xlabel('Time ($\mu s$)')
				pyp.ylabel('ADC counts')
				pyp.legend(loc='upper left')

				# save the figures
				pyp.figure(1)
				pyp.savefig("/u/data/leap/plots/compare_filtered_spectrum_%s-%s.png"%(fnumber, fsec) )
				pyp.figure(2)
				pyp.savefig("/u/data/leap/plots/compare_filtered_phase_%s-%s.png"%(fnumber, fsec) )
				pyp.figure(3)
				pyp.savefig("/u/data/leap/plots/compare_filtered_psd_%s-%s.png"%(fnumber, fsec) )
				pyp.figure(4)
				pyp.savefig("/u/data/leap/plots/compare_filtered_wfm_%s-%s.png"%(fnumber, fsec) )

			
			#print "Waveform means and RMS's"
			#print "unfiltered", numpy.mean(wv), numpy.std(wv)
			#print "filtered", numpy.mean(wv), numpy.std(wv)	
			
			#print "Fourier amplitudes for frequency ", freq[10], freq[50]
			#print "unfiltered,", fname,",", freq[10],",", ft[10]
			#print "unfiltered,", fname,",", freq[50],",", ft[50]
			#print "filtered,", ffname,",", ffreq[10], ",", fft[10]
			#print "filtered,", ffname, ",", ffreq[50], ",", fft[50]

			
			# chunk number, tuning, polarization, unfiltered mean & rms, filtered mean & rms
			fwfm.write("%d,%d,%d,%e,%e,%e,%e\n"%(ichunk,itune,ipol,numpy.mean(wv),numpy.std(wv), numpy.mean(fwv), numpy.std(fwv)))
			
			# chunk number, tuning, polarization, unfiltered freq & fourier amp at two frequencies, filtered freq & fourier amp at two frequencies
			ffd.write("%d,%d,%d,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e\n"%(ichunk,itune,ipol,freq[10],numpy.abs(ft[10]),numpy.angle(ft[10]), freq[50],numpy.abs(ft[50]),numpy.angle(ft[50]),ffreq[10],numpy.abs(fft[10]),numpy.angle(fft[10]), ffreq[50],numpy.abs(fft[50]),numpy.angle(fft[50])))

fwfm.close()
ffd.close()
#pyp.show()

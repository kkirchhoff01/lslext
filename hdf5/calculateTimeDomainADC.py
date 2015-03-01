#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
calculateTimeDomainADC.py - Read in a DRX/HDF5 wataerfall file and calculate the noise temperature  (mean and RMS) for each observation (XX and YY or I). 

Usage:
./calculateTimeDomainADC.py [OPTIONS] file

$Rev$
$LastChangedBy$
$LastChangedDate$
"""

import os
import sys
import h5py
import numpy
import getopt
from datetime import datetime

from lsl.statistics import robust, kurtosis


def usage(exitCode=None):
	print """calculateTimeDomainADC.py - Read in DRX/HDF5 waterfall file and calculate the time domain ADC means and rms's.
Usage: calculateSK.py [OPTIONS] file

Options:
-h, --help                Display this help information
-n, --no-update           Do not add the pSK information to the HDF5 file
"""
	
	if exitCode is not None:
		sys.exit(exitCode)
	else:
		return True


def parseOptions(args):
	config = {}
	# Command line flags - default values
	config['update'] = True
	config['duration'] = 1.0
	config['args'] = []
	
	# Read in and process the command line flags
	try:
		opts, args = getopt.getopt(args, "hd:n", ["help","duration", "no-update"])
	except getopt.GetoptError, err:
		# Print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage(exitCode=2)
		
	# Work through opts
	for opt, value in opts:
		if opt in ('-h', '--help'):
			usage(exitCode=0)
		elif opt in ('-d', '--duration'):
			config['duration'] = float(value)
		elif opt in ('-n', '--no-update'):
			config['update'] = False
		else:
			assert False
			
	# Add in arguments
	config['args'] = args
	
	# Return configuration
	return config


def main(args):
	config = parseOptions(args)
	
	filename = config['args'][0]
	
	# Open the file and loop over the observation sections
	h = h5py.File(filename, mode='a' if config['update'] else 'r')
	for obsName in h.keys():
		obs = h.get(obsName, None)
		
		# Load in the information we need to calculate the mean and rms ADC counts
		tInt = obs.attrs['tInt']
		srate = obs.attrs['sampleRate']
		
		chunkSize = int(round(config['duration']/tInt))
		
		print "Staring Observation #%i" % int(obsName.replace('Observation', ''))
		print "  Sample Rate: %.1f Hz" % srate
		
		time = obs.get('time', None)[:]
		tuning1 = obs.get('Tuning1', None)
		tuning2 = obs.get('Tuning2', None)
		
		
		# Loop over data products
		for dp in ('XX', 'YY'):
			mod1 = tuning1.get(dp+'mag', None)
			phase1 = tuning1.get(dp+'phase', None)
			mod2 = tuning2.get(dp+'mag', None)
			phase2 = tuning2.get(dp+'phase', None)
			ft1 = mod1[:][:]*numpy.cos(phase1[:][:]) + 1j*mod1[:][:]*numpy.sin(phase1[:][:])
			ft2 = mod2[:][:]*numpy.sin(phase2[:][:]) + 1j*mod2[:][:]*numpy.sin(phase2[:][:])
			data1 = numpy.fft.ifft(numpy.fft.ifftshift(ft1))
			data2 = numpy.fft.ifft(numpy.fft.ifftshift(ft2))

			if data1 is None:
				continue
			
			# Loop over chunks for computations
			adc1 = numpy.zeros_like(data1)
			adc2 = numpy.zeros_like(data2)
			rms1 = numpy.zeros_like(data1)
			rms2 = numpy.zeros_like(data2)

			for i in xrange(time.size/chunkSize+1):
				start = i*chunkSize
				stop = start + chunkSize
				if stop >= time.size:
					stop = time.size - 1
				if start == stop:
					continue
					
				## Compute the mean and rms for each channel in both tunings
				section1 = data1[start:stop,:]
				section2 = data2[start:stop,:]
				for j in xrange(section1.shape[1]):
					adc1[start:stop, j] = numpy.mean(section1[:,j])
					adc2[start:stop, j] = numpy.mean(section2[:,j])
					rms1[start:stop, j] = numpy.std(section1[:,j])
					rms2[start:stop, j] = numpy.std(section2[:,j])
					
						
			# Report
			print "  => %s-1 Tuning 1 Mean: %.3f" % (dp, numpy.nanmean(abs(adc1)))
			print "     %s-1 Tuning 1 Std. Dev.: %.3f" % (dp, numpy.nanmean(rms1))
			print "     %s-2 Tuning 2 Mean: %.3f" % (dp, numpy.nanmean(abs(adc2)))
			print "     %s-2 Tuning 2 Std Dev.: %.3f" % (dp, numpy.nanmean(rms2))
			
			# Save the information to the HDF5 file if we need to
			if config['update']:
				h.attrs['FileLastUpdated'] = datetime.utcnow().strftime("UTC %Y/%m/%d %H:%M:%S")
				
				## Tuning 1
				td1 = tuning1.get('ADC', None)
				if td1 is None:
					td1 = tuning1.create_group('ADC')
				try:
					td1.create_dataset(dp+'mag', adc1.shape, 'f4')
				except:
					pass
				td1[dp+'mag'][:,:] = adc1
				td1.attrs['mean'] = numpy.nanmean(abs(adc1))
				td1.attrs['rms'] = numpy.nanmean(rms1)
							
				## Tuning 2
				td2 = tuning2.get('ADC', None)
				if td2 is None:
					td2 = tuning1.create_group('ADC')
				try:
					td2.create_dataset(dp+'mag', adc2.shape, 'f4')
				except:
					pass
				td2[dp+'mag'][:,:] = adc1
				td2.attrs['mean'] = numpy.nanmean(adc2)
				td2.attrs['rms'] = numpy.nanmean(rms)	
				
	# Done!
	h.close()


if __name__ == "__main__":
	main(sys.argv[1:])
	


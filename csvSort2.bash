#!/bin/bash
# Script for seperating DRX files into simple, usable data sets in csv format

for i in $@; do
  echo "beam,tuning,tunefreq,polarity,real,imag" > ${i}_t1p0.csv
  echo "beam,tuning,tunefreq,polarity,real,imag" > ${i}_t1p1.csv
  echo "beam,tuning,tunefreq,polarity,real,imag" > ${i}_t2p0.csv
  echo "beam,tuning,tunefreq,polarity,real,imag" > ${i}_t2p1.csv
 
  /u/data/swissel/software/anaconda/bin/python drxCsvMaker.py ${i} | awk -v temp="${i}" -F "," '
  BEGIN {
  } {
    tune=$2;
    pol=$4
    if ( tune == 1 && pol == 0) {
      print $0 > temp "_t1p0.csv";
    } else if ( tune == 1 && pol == 1 ) {
      print $0 > temp "_t1p1.csv"; 
    } else if ( tune == 2 && pol == 0 ) {
      print $0 > temp "_t2p0.csv"; 
    } else if ( tune == 2 && pol == 1 ) {
      print $0 > temp "_t2p1.csv"; 
    }
   } END {
   }'
done
mv ~/data/*.csv ~/data/csv 


#!/bin/bash


for i in $@; do
  echo "beam,tuning,polarity,real,imag" > ${i}_t1p0.csv
  echo "beam,tuning,polarity,real,imag" > ${i}_t1p1.csv
  echo "beam,tuning,polarity,real,imag" > ${i}_t2p0.csv
  echo "beam,tuning,polarity,real,imag" > ${i}_t2p1.csv
  /u/data/swissel/software/anaconda/bin/python drxCsvMaker.py ${i} > ${i}wip.csv
done

#STILL NEED TO ADD SORTER
#for j in $(ls | grep wip); do
#  for k in $(cat ${j}); do
    

mv ~/data/*.csv ~/data/csv 


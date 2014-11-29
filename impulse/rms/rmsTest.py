from rmsIterator import rmsIterator
from rmsMaster import rmsMaster
from datetime import datetime

timer = datetime.now()

#rmsMaster takes: inputpath, outputpath, framesperchunk, and totalchunks for init parameters
hf_on = rmsMaster('/u/data/leap/observations/056777_000085153', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_hf_on.png',15,20)
hf_off = rmsMaster('/u/data/leap/observations/056777_000085150', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_hf_off.png',15,20)
lf_on = rmsMaster('/u/data/leap/observations/056777_000085153', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_lf_on.png',15,20)
lf_off = rmsMaster('/u/data/leap/observations/056777_000085153', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_lf_off.png',15,20)

print "Init complete."

hf_on.compute()

print "HF On complete"

hf_off.compute()

print "HF Off complete"

lf_on.compute()

print "LF On complete"

lf_on.compute()

print "LF Off complete\nProcessing complete in " + str(datetime.now()-timer) + "\n"

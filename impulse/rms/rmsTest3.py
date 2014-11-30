from rmsIterator import rmsIterator
from rmsMaster import rmsMaster
from datetime import datetime
import thread
timer = datetime.now()

#rmsMaster takes: inputpath, outputpath, framesperchunk, and totalchunks for init parameters
'''
hf_on = rmsMaster('/u/data/leap/observations/056777_000085153', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_hf_on.png',15,650000)
hf_off = rmsMaster('/u/data/leap/observations/056777_000085150', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_hf_off.png',15,650000)
'''
lf_on = rmsMaster('/u/data/leap/observations/056777_000085151', '/u/data/iqwofford/figures/rmsIteratorOutput/04302014_lf_on.png',15,650000)

'''
lf_off = rmsMaster('/u/data/leap/observations/056777_000085152', '/u/home/qwofford/figures/rmsIteratorOutput/04302014_lf_off.png',15,650000)
'''
print "Init complete."
'''
try:
    print 'Beginning Hf On thread'
    thread.start_new_thread(hf_on.compute())
except:
    print 'Did not start HF On thread'
print 'HF On complete'
try:
    'Beginning Hf off thread'
    thread.start_new_thread(hf_off.compute())
except:
    print 'Did not start HF Off thread'
print 'HF Off complete'
'''
try:
    print 'Beginning Lf On thread'
    thread.start_new_thread(lf_on.compute())
except:
    print 'Did not start Lf On thread'
print 'LF On complete'
'''
try:
    print 'Beginning Lf Off thread'
    thread.start_new_thread(lf_off.compute())
except:
    print 'Did not start Lf Off thread'

print "LF Off complete"
'''
print "Processing complete in " + str(datetime.now()-timer) + "\n"

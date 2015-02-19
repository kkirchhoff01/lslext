import sys
from rmsIterator import rmsIterator
from rmsMaster import rmsMaster
from datetime import datetime
import thread
timer = datetime.now()

#Check to be sure command line arguments are present. Format is: fileinput, fileoutput, chunksize, numberofchunks
print "You supplied " + str(len(sys.argv)-1) + " command line arguments.\nThey are: " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]) + " " + str(sys.argv[4]) + "\n"

rmsMaker = rmsMaster(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

print "Init complete."
print "Processing " + str(sys.argv[4]) + " chunks of " + str(sys.argv[3]) + " frames each."
print 'Beginning compute method'
rmsMaker.compute()
print "Command line arguments were: \n" + str(sys.argv[0]) + " " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]) + str(sys.argv[4]) + "\n"
print "Processing complete in " + str(datetime.now()-timer) + "\n"

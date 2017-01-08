#!/usr/bin/python2

import sys
import subprocess
import thread

import logging 
import redis_com

from  listener import hf_sancov_listener

#from symbol import tracing_func
from driller_call import test_drilling

logging.getLogger("tracer").setLevel(logging.DEBUG)
logging.getLogger("driller").setLevel(logging.DEBUG)

def usage():
    print "Usage " + sys.argv[0] + " <Honggfuzz directory> " + \
	" <input files> "+\
	" <binary> "+\
	 " <output directory> \n"+\
	"Runs honggfuzz and concolic execution"
    exit(1)

def main():
    logging.basicConfig(filename = 'temp.log', level = logging.DEBUG)
    if len(sys.argv) < 4:
        usage()
    #print sys.argv
    #Assign arguments to variables
    honggfuzz_directory = sys.argv[1]
    input_files_directory = sys.argv[2]
    binary_fuzzed = sys.argv[3]
    binary_name = binary_fuzzed.rsplit('/',1)[-1]
    output_directory = "." if len(sys.argv) != 5 else sys.argv[4]
    #open log file
    logFile = open(output_directory + "logFile","w")
    logErr =open (output_directory + "logErr","w")
    #open queue file
    #queueFile = open("queueFile","rw")
    #.run ./../honggfuzz/honggfuzz -f ../../honggfuzz/examples/inputfiles/ -C -- ../../honggfuzz/examples/targets/badcode1 ___FILE___
    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",input_files_directory,"-W",output_directory,"-C","--",binary_fuzzed,"___FILE___ "],stdout=logFile, stderr=logErr)
    #Create listener on HF_SANCOV FILE that creates a new sancov file for every raw file created
    red=redis_com.connect_redis()
    thread.start_new_thread(hf_sancov_listener,("Thread-1",binary_fuzzed, output_directory, red))
    #Begin symbolic/Concolic execution thread for every missed pc
    while(1):
	#tracing_func(binary_fuzzed,input_files_directory)
	test_drilling(binary_fuzzed,input_files_directory,red)

if __name__ == '__main__':
   main()

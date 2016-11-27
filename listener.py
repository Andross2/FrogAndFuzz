import glob
import os
import re
import redis_com

import sancov_script

def hf_sancov_listener(threadName,binary_fuzzed, directory):
    queueFile = open("queueFile","r+")
    red=redis_com.connect_redis()
    while(1):
	file_list_sancov = []
	file_list_raw = []
	#Get newest sancov.raw
	newest_raw = min(glob.iglob(directory+'/HF_SANCOV/*.raw'), key=os.path.getctime)
	#create a sancov file
	file_list_raw.append(newest_raw)
	file_list_sancov = (sancov_script.RawUnpack(file_list_raw))
	#Print covered PCS
	#print file_list_sancov[0]
	file_list_sancov = re.findall(r'\b(\S+.sancov)\b',str(file_list_sancov[0]))
	#print file_list_sancov
	covered_pc = sancov_script.PrintFiles(file_list_sancov)
	# printing the missing PC
	missed_pc = sancov_script.PrintMissing(binary_fuzzed,covered_pc)
	#print missed_pc
	#Save to queue file
	queueFile.write('-----------------------------\n')
	for pc in missed_pc:
		queueFile.write(pc + '\n')
        redis_com.add_Sancov(binary_fuzzed,red,pc)
	# TODO SAVE TO REDIS DB
#	for pc in missed_pc:
#		print queueFile
#		queueFile.write(pc)

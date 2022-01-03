import time
import subprocess 
import os 
import sys 

import statistics as st

# README: Script only available for BirdID time measurement, BirdNET use a different method 
# Load this script along with the variation of the predictSingle.py (predictSingleFull)
# in the folder that is going to be mounted in the BirdID container. After that, copy/move these
# two files into the workspace folder and execute in there this script


elapsed = []
audios = os.listdir("./data/")
for audio in audios:
	if(audio.endswith("wav")):
		pathToAudio = "./data/" + audio
		start = time.time()
		predSingle_out = subprocess.check_output([sys.executable, "predictSingleFull.py", pathToAudio])
		end = time.time()
		
		howLong = end-start
		elapsed.append(howLong)
		
		print("Time taken: ", howLong)

with open("timeBirdID.txt", "a+") as file:
	file.write(elapsed)
	
print("Average time taken: ", st.mean(elapsed), " (+-",st.stdev(elapsed),")")


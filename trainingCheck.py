import sys
import os
import subprocess
import json
import csv
import numpy as np

# ---------------------- METHODS ----------------------
def getOutputDict(output):
	return json.loads(output)

# -----------------------------------------------------


# Get list of NL audio recordings
path = "data/xenocantoNL/audioFiles/"
dirListing = os.listdir(path)
audioFiles = []

for item in dirListing:
	if ('.' not in item):
		audioFiles.append(item)

# Possible labels/classes
labels = []

ClassIdsFid = 'ClassIds.txt'
ClassIds = np.loadtxt(ClassIdsFid, dtype=np.str, delimiter='\t')


with open('BirdsEurope254MetadataDict.json', encoding='utf-8') as data_file:
    BirdsEurope254MetadataDict = json.load(data_file)

for ClassId in ClassIds: 
    labels.append(BirdsEurope254MetadataDict[ClassId]['NameLat'])
labels = sorted(labels)

# CSV List
toCSV = []

indCount = 1
# Make predicts from each audio file
for audioId in audioFiles:
	pathToAudio = "./data/xenocantoNL/audioFiles/" + str(audioId)
	# Call precit script (classifier)
	predSingle_out = subprocess.check_output([sys.executable, "predictSingleFile.py", pathToAudio])
	
	# Create default dictionary
	x = ['FileId']
	header = x + labels
	values = [str(audioId)] + ([0] * len(labels))
	audioDic = dict(zip(header, values))

	# Change prob of labels that are obtained from predict script
	strOutput = predSingle_out.decode("utf-8") #From bytes to str
	outputDict = getOutputDict(strOutput)

	for pred in outputDict:
		audioDic[pred['scieName']] = pred['prediction']

	toCSV.append(audioDic)
	percentage = indCount * 100 / len(audioFiles)
	print("Audio "+str(audioId)	+" analyzed." + " -- " + str(indCount) + " out of " + str(len(audioFiles)) + "("+str(percentage)+" %)")
	indCount += 1

# Create file as CSV
with open('data/recordingsNL.csv', 'w+', newline='')  as output_file:
	dict_writer = csv.DictWriter(output_file, header)
	dict_writer.writeheader()
	dict_writer.writerows(toCSV)
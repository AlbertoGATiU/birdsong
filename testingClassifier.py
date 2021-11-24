import json
import csv
from statistics import mean

import numpy as np
import matplotlib.pyplot as plt

def getPredictionForClass(predictions, label):
	for key, value in predictions.items():
		if(key == label):
			return value
	return 0

def listMean(numList):
	return sum(numList)/float(len(numList))

def getMostProbClass(entryDic):
	labels = list(entryDic.keys())
	probs = list(entryDic.values())
	# Remove file id from lists
	del labels[0]
	del probs[0]
	
	# Index where max prob is found 
	maxVal = max(probs)
	maxInd = probs.index(maxVal)
	
	return labels[maxInd]

def getConfusion(mostProbClass, realClass):
	if (mostProbClass == realClass == targetName):
		return 0
	if (mostProbClass != targetName and realClass != targetName):
		return 1
	if (mostProbClass == targetName and realClass != targetName):
		return 2
	if (mostProbClass != targetName and realClass == targetName):
		return 3
# -----------------------------------------------------------------------------
targetName = "Turdus merula"

realLabels = []
predList = []

################################## FILES ################################## 
# Open real-class file 
with open('classLabels.txt','r') as fRealClasses:
	lines = fRealClasses.readlines()
	for line in lines:
		recId, realLabel = line.split(",")
		realLabels.append({'audioId':recId, 'class':realLabel})

# Open predictions CSV
with open('recordingsNL.csv') as f:
    predList = [{k: float(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

############################ EVALUATION METRICS ############################  
# Blackbird accuracy
bbAccuracy = []
# Confusion: TP, TN, FP, FN
confusion = [0, 0, 0, 0]

for pred in predList:
	predFileId = str(pred['FileId']).replace(".0", "")
	mostPredClass = getMostProbClass(pred)
	for entry in realLabels:
		audioId = entry['audioId'].replace("\n","")
		classLabel = entry['class'].replace("\n","")
		
		# Check confusion (True positive/negative or false positive/negative)
		if (audioId == predFileId):
			confusion[getConfusion(mostPredClass, classLabel)] += 1

		# Checking test set with Turdus Merula (FOR ACCURACY)
		if(classLabel == targetName):
			# If audio ID is from test set
			if(predFileId == audioId):
				bbProb = getPredictionForClass(pred, classLabel)
				#print("Audio "+audioId+" --> "+str(bbProb))
				bbAccuracy.append(float(bbProb))

########################################### EVALUATION PRINTS ###########################################
#print(len(bbAccuracy))
format_acc = "{:.2f}".format(100*listMean(bbAccuracy))
print("Blackbird mean accuracy: ", str(format_acc), " %")
print("\n ################### Confussion metrics: ###################")
print("True Positives  (TP): ", confusion[0])
print("True Negative   (TN): ", confusion[1])
print("Flase Positives (FP): ", confusion[2])
print("False Negative  (FN): ", confusion[3])
precision = confusion[0]/(confusion[0]+confusion[2])
recall = confusion[0]/(confusion[0]+confusion[3])
print("\nPrecision: ", precision)
print("Recall: ", recall)
f1_score = 2*(precision*recall)/(precision+recall)
print("\nF1 Score: ", f1_score)
print("##############################################################")
# Calculate probability distribution
n, bins, patches = plt.hist(bbAccuracy)
#plt.show()

# Other way
from scipy.stats import norm
import statistics
from scipy import stats

bbMean = statistics.mean(bbAccuracy)
bbStd = statistics.stdev(bbAccuracy)
bbPDF = norm.pdf(bbAccuracy, bbMean, bbStd)

plt.bar(bbAccuracy, bbPDF)
plt.show()
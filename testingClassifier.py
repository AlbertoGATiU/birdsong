import json
import csv
from statistics import mean

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score

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
# ROC values
y_true = []
y_pred = []

for pred in predList:
	predFileId = str(pred['FileId']).replace(".0", "")
	mostPredClass = getMostProbClass(pred)
	for entry in realLabels:
		audioId = entry['audioId'].replace("\n","")
		classLabel = entry['class'].replace("\n","")
		
		# Check confusion (True positive/negative or false positive/negative)
		# Check only if label is not "Mystery mystery"
		if (audioId == predFileId and classLabel != "Mystery mystery" and classLabel != "Sonus Naturalis"):
			confusion[getConfusion(mostPredClass, classLabel)] += 1
			# ROC
			# True labels
			if (classLabel == targetName): y_true.append(1)
			else: y_true.append(0)
			# Pred labels
			if (mostPredClass == targetName): y_pred.append(1)
			else: y_pred.append(0)

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
specif = confusion[1]/(confusion[1]+confusion[2])
print("\nPrecision: ", precision)
print("Recall: ", recall)
print("\nSensitivity: ", recall)
print("Specificity: ", specif)
f1_score = 2*(precision*recall)/(precision+recall)
print("\nF1 Score: ", f1_score)
fpr, tpr, _ = roc_curve(y_true,y_pred)
auc_score = roc_auc_score(y_true, y_pred)
print("\nAUC Score: ", auc_score)
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
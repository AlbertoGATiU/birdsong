import csv
import sys
import subprocess
import os 

import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score


############### METHODS ###############

def getMostPredClasses(dict_list):
	mostPred = []
	confThres = 0.60

	for timePred in dict_list:
		for item in timePred.items():
			# Get lists of values and keys
			values = item[1].split(";")
			keys = item[0].split(";")

			# Iterate through values/keys
			for i in range(len(values)):
				value = values[i]
				key = keys[i]
				if(float(value) > confThres and 
				   key not in mostPred and 
				   key != "StartTime [s]" and
				   key != "EndTime [s]"):
					mostPred.append(key)
	
	return mostPred

def getConfusion(mostProbClasses, realClass):
	if (targetClass in mostProbClasses and realClass == targetClass):
		return 0
	if (targetClass not in mostProbClasses and realClass != targetClass):
		return 1
	if (targetClass in mostProbClasses and realClass != targetClass):
		return 2
	if (targetClass not in mostProbClasses and realClass == targetClass):
		return 3

################ MAIN ################

nameFormat = "_c1_sorted.csv"

bbPreds = []
y_true = []
y_pred = []
# Confussion TP; TN; FP; FN
confusion = [0, 0, 0, 0]

counter = 0


# Open real-class file 
realLabels = []
predTxtPath = "./transfFiles/sortedCSV_c1/"
filesInPath = os.listdir(predTxtPath)
targetClass = "Turdus merula"

with open('classLabels.txt','r') as fRealClasses:
	lines = fRealClasses.readlines()
	for line in lines:
		recId, realLabel = line.split(",")
		realLabel = realLabel.replace("\n","")
		realLabels.append({'audioId':recId, 'class':realLabel})

for file in filesInPath:
	# Take only CSV files with proper format name
	if(file.endswith(nameFormat)):
		# Obtain Id and class predicted above a threshold
		audioId = file.replace(nameFormat,"")
		audioId = audioId.replace(" ","")
		# Open CSV file with predictions 	
		with open(predTxtPath+str(file)) as f:
		    dict_pred = [{k: str(v) for k, v in row.items()}
		        for row in csv.DictReader(f, skipinitialspace=True)]
		
		# Get predicted classes (with threshold)
		pred_classes = getMostPredClasses(dict_pred)

		# Check with the REAL LABELS txtfile
		if (audioId in [ sub['audioId'] for sub in realLabels ]):
			counter += 1
			dictEntry = next((sub for sub in realLabels if sub['audioId'] == audioId), None)
			realClass = dictEntry['class']

			confusion[getConfusion(pred_classes, realClass)] += 1
			
			# Check Blackbird accuracy
			if (realClass == targetClass):
				if (realClass in pred_classes): 
					bbPreds.append(1)
				else:
					bbPreds.append(0)
			# ROC
			# True labels
			if (realClass == targetClass): y_true.append(1)
			else: y_true.append(0)
			# Pred labels
			if (targetClass in pred_classes): y_pred.append(1)
			else: y_pred.append(0)
		

print("COUNTER: ", counter)
####################### EVALUATION METRICS ########################
bbAcc = (confusion[0]+confusion[1])/(confusion[0]+confusion[1]+confusion[2]+confusion[3])
format_acc = "{:.2f}".format(100*bbAcc)
precision = confusion[0]/(confusion[0]+confusion[2])
recall = confusion[0]/(confusion[0]+confusion[3])
specif = confusion[1]/(confusion[1]+confusion[2])
f1_score = 2*(precision*recall)/(precision+recall)
fpr, tpr, _ = roc_curve(y_true,y_pred)
auc_score = roc_auc_score(y_true, y_pred)

print("\n ################### BirdNET Evaluation Metrics: ###################")
print("Blackbird mean accuracy: ", str(format_acc), " %\n")
print("True Positives  (TP): ", confusion[0])
print("True Negative   (TN): ", confusion[1])
print("False Positives (FP): ", confusion[2])
print("False Negative  (FN): ", confusion[3])
print("\nPrecision: ", precision)
print("Recall: ", recall)
print("\nSensitivity: ", recall)
print("Specificity: ", specif)
print("\nF1 Score: ", f1_score)
print("\nAUC Score: ", auc_score)
print("##############################################################")

# Plot ROC curve
plt.plot(fpr, tpr, linestyle='--',color='green')
# title
plt.title('ROC curve')
# x label
plt.xlabel('False Positive Rate')
# y label
plt.ylabel('True Positive rate')

plt.legend(loc='best')

plt.show();


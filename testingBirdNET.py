import os

import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score

############################# METHODS ##############################
def getMostPredClasses(filePath):
	mostPred = []
	confThres = 0.50
	with open(filePath) as f:
		#print("\nANALYSING FILE ", filePath)
		lines = f.readlines()
		# Remove header
		del lines[0]
		if (len(lines) > 0):
			# Obtain species and their probabilities
			probs = []
			for line in lines: 
				line = line.strip() # Remove extra white spaces
				line = line.replace("\t", ";")
				entry = line.split(";")
				if(float(entry[10]) >= confThres and entry[9] not in mostPred):
					mostPred.append(entry[9])
					probs.append(entry[10])
		else:
			mostPred.append("Null")
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


#################################### MAIN ##########################
targetClass = "Eurasian Blackbird"
predTxtPath = "/home/alberto/birdsong/dataset/xenocantoNL/predTxt/"
filesInPath = os.listdir(predTxtPath)

# Open real-class file 
realLabels = []
with open('classCommonLabels.txt','r') as fRealClasses:
	lines = fRealClasses.readlines()
	for line in lines:
		recId, realLabel = line.split(",")
		if (realLabel == "Common Blackbird\n"): realLabel = "Eurasian Blackbird\n"
		realLabels.append({'audioId':recId, 'class':realLabel})

bbPreds = []
y_true = []
y_pred = []
# Confussion TP; TN; FP; FN
confusion = [0, 0, 0, 0]
for file in filesInPath:
	if(file.endswith(".txt")):
		# Obtain Id and class predicted above a threshold
		audioId = file.split(".")[0]
		pred_classes = getMostPredClasses(predTxtPath+str(file))

		# Check with the REAL LABELS txtfile
		if (audioId in [ sub['audioId'] for sub in realLabels ]):
			dictEntry = next((sub for sub in realLabels if sub['audioId'] == audioId), None)
			realClass = dictEntry['class'].replace("\n","")

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

####################### EVALUATION METRICS ########################
bbAcc = sum(bbPreds)/len(bbPreds)
format_acc = "{:.2f}".format(100*bbAcc)
precision = confusion[0]/(confusion[0]+confusion[2])
recall = confusion[0]/(confusion[0]+confusion[3])
specif = confusion[1]/(confusion[1]+confusion[2])
f1_score = 2*(precision*recall)/(precision+recall)
fpr, tpr, _ = roc_curve(y_true,y_pred)
auc_score = roc_auc_score(y_true, y_pred)

print("\n ################### Evaluation metrics: ###################")
print("Blackbird mean accuracy: ", str(format_acc), " %\n")
print("True Positives  (TP): ", confusion[0])
print("True Negative   (TN): ", confusion[1])
print("Flase Positives (FP): ", confusion[2])
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

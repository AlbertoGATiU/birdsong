import statistics as st
import matplotlib.pyplot as plt 
import numpy as np

def getTimeInPercentiles(times, percentages):
	timedPerc = []
	
	for perc in percentages:
		npTimes = np.array(times)
		timedPerc.append(np.percentile(npTimes, perc))

	return timedPerc

fileName = "loadDataSeq.txt"

st_codes = []
ok_codes = 0
err_codes = 0

times = []
totalTime = 0

nFiles = 0

# Obtain values from file where response times and stats codes are stored
with open(fileName) as file:
	lines = file.readlines()
	for line in lines:
		line = line.strip()
		if (line.startswith("Response")):
			nFiles += 1
			code = int(line.split(" ")[12])
			st_codes.append(code)
			if code == 200: 
				ok_codes += 1
				times.append(float(line.split(" ")[8]))
			elif code == 500: 
				err_codes += 1

		else:
			totalTime = line.split(" ")[2]

# Time metrics 
mean = st.mean(times)
med = st.median(times)
minim = min(times)
maxim = max(times)


print("Mean time:", mean)
print("Median time:", med)
print("\nMax time:",maxim)
print("Min time:",minim)
print("\nTotal time:", totalTime)
#print("\nStatus codes: ", st_codes)


################## GRAPHS ##################


########### MIN MAX MEAN MED TIME ###########
metrics = ["Min", "Median", "Mean", "Max"]
values = [minim, med, mean, maxim]

fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(metrics, values, color ='maroon',
        width = 0.4)
 
plt.xlabel("Metrics")
plt.ylabel("Values")
plt.title("Mean, median, min and max of the time taken")
plt.show()

########### PERCENTILE TIMES ########### 
validPercetages = [50, 55, 60, 65, 70, 75, 80, 75, 90, 95]
times = getTimeInPercentiles(times, validPercetages)

fig = plt.figure(figsize = (10, 5))

# creating the bar plot
plt.bar(validPercetages, times, color ='maroon',
        width = 0.4)
 
plt.xlabel("Percentage of request within response time")
plt.ylabel("Time taken")
plt.title("Time taken to process requests")
plt.show()


########### CODES ###########
codes = ["Total requests", "OK (200)", "Error (500)"]
codesCount = [nFiles, ok_codes, err_codes]

fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(codes, codesCount, color ='maroon',
        width = 0.4)
 
plt.xlabel("Request types")
plt.ylabel("Number of requests")
plt.title("Requests within response time")
plt.show()
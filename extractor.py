import requests
import json


######################### FUNCTIONS ############################################
def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def checkFile(recId):
    fName = "classLabels.txt"
    alreadyDL = False
    with open(fName, 'r') as classLabels:
        lines = classLabels.readlines()
        for i in lines:
            if str(recId) == i.rpartition(',')[0]:
                alreadyDL = True
                break
    return alreadyDL



################################################################################

print("Extracting NL birds dataset")
# For each page in the URL request...
nPages = 28
for i in range(nPages):
    requestsURL = "https://www.xeno-canto.org/api/2/recordings?query=cnt:netherlands&page=" + str(i+1)
    # Make request
    response = requests.get(requestsURL)
    json_obj = response.json()

    print("Page " + str(i+1) + " out of " + str(nPages))
    print("Request: " + requestsURL)
    # Get recording
    recordings = json_obj["recordings"]

    # Iterate through them
    for i in range(len(recordings)):
        # Get download URL and recording id
        downloadURL = recordings[i]["file"] 
        downloadURL = "https:"+downloadURL
        recordId = recordings[i]["id"]
        fileName = "audioFiles/"+ recordId

        existing = checkFile(recordId)
        if(existing == True):
            print("File with id " + recordId + " already written")
        else:
            with open('classLabels.txt', 'a+') as classLabels:
                # Get class and write it in file
                label = recordId+","+recordings[i]["gen"]+ " " +recordings[i]["sp"]+"\n"
                classLabels.write(label)

                # Download file
                downloadReq = requests.get(downloadURL)
                audioFile = open(fileName, 'wb').write(downloadReq.content)
                print("Finished downloading... " + str(recordId) + "(" + str(i+1) + ")")

print("Extraction finished!")
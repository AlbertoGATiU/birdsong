import statistics as st
import re

# README: This script takes the results from the command 'docker stats <container_id>' stored
# in a file (one for each model) and calculates the mean and standard deviation of the CPU and
# memory usage. The creation/writing of those files is done before. 


ID_cpu_usg = []
ID_mem_usg = []
NET_cpu_usg = []
NET_mem_usg = []

fileName_ID = "BirdID_stats.txt"
fileName_NET = "BirdNET_stats.txt"

def getCPU_mem_usage(fileName):
	cpu = []
	mem = []
	with open(fileName, "r+") as file:
		lines = file.readlines()
		for line in lines:
			if ("MEM USAGE" not in line):	
				elems = re.sub(' +', ' ', line).split(" ")

				cpu.append(float(elems[2].replace("%","")))
				mem.append(float(elems[6].replace("%","")))

	return cpu, mem

# BIRD ID STATISTICS FILE
ID_CPU_usg, ID_mem_usg = getCPU_mem_usage(fileName_ID)
NET_CPU_usg, NET_mem_usg = getCPU_mem_usage(fileName_NET)

print("BirdID CPU and Memory usage: ")
print("CPU usage (%)", st.mean(ID_CPU_usg), "% (+-",st.stdev(ID_CPU_usg),")")
print("Memory usage (%)", st.mean(ID_mem_usg), "% (+-",st.stdev(ID_mem_usg),")")

print("\nBirdNET CPU and Memory usage: ")
print("CPU usage (%)", st.mean(NET_CPU_usg), "% (+-",st.stdev(NET_CPU_usg),")")
print("Memory usage (%)", st.mean(NET_mem_usg), "% (+-",st.stdev(NET_mem_usg),")")

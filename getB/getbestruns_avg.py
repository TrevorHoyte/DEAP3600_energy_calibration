# this makes the average B parameter in every 5 day window in the data, make sure the abc_file created by abc_making.py is in the "dir_output".
# this file creates a new txt file with the averaged B parameters per 5 day window, here its called abc_official_interpolation_points_avg.txt
import ROOT
import numpy
import array 
import glob
import math
import re
import couchdb
import sys
from datetime import datetime
import time
from  statistics import median_low
import statistics

dir_output="/home/trevorh/trevor_branch/ambe_correction/final_go/official/"

abc_file="abc_a19_cfixed.txt"

outfile="abc_official_interpolation_points_avg.txt"

server = couchdb.Server('https://deimos.physics.carleton.ca:6984')
db = server['deapdb']
def find_time(runNumber):
    docid = "RUNINFO_config_" + str(runNumber) + "_" + str(runNumber)
    doc = db[docid]
    #print(doc["dateTimeStart"])
    a=datetime.strptime(doc["dateTimeStart"], "%a %b %d %H:%M:%S %Y")
    return a

runlist=[]
abc_data=open(dir_output+abc_file,"r")
lines=abc_data.readlines()
for line in lines:
    val=line.strip("()\n").split(",")
    runlist.append((int(float(val[0])),float(val[1]),float(val[2]),float(val[3])))

runlist.sort(key=lambda x:x[0])
print(runlist)
print(len(runlist))
#runlist(runid,a,b,c)

   
f=open(dir_output+outfile,"w")

k=0
while k<=len(runlist):
    
    id_current=runlist[k][0]
    t1=find_time(id_current)
    abclist=[]
    abc_start=(runlist[k])
    abclist.append(abc_start)
    for i in range(k+1,len(runlist)):
        id_next=runlist[i][0]
        t2=find_time(id_next)
        delta = t2 - t1
        deltat=delta.days
        if deltat>5 or i==len(runlist):
            k=i
            mean_b=[]
            print(id_current)
            
            for item in abclist:
                print(item)
                mean_b.append(item[2])
            parameterb=statistics.mean(mean_b)
             
            print("Average B VALUES")
            print(parameterb)
            f.write("( %s,-19.51,%s,548)\n"%(id_current,parameterb))
            print("\n\n\n\n")
            break
        
        abclist.append(runlist[i])
        
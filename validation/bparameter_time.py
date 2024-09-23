# this plots the B parameter vs time, you need to have the file containing the B parameter by run in the dir output, and the name of the file as abc_file


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

dir_output="/home/trevorh/trevor_branch/ambe_correction/final_go/official/"

abc_file="abc_a19_cfixed.txt"
abc_data=open(dir_output+abc_file,"r")


server = couchdb.Server('https://deimos.physics.carleton.ca:6984')
db = server['deapdb']
def find_time(runNumber):
    docid = "RUNINFO_config_" + str(runNumber) + "_" + str(runNumber)
    doc = db[docid]
    #print(doc["dateTimeStart"])
    a=datetime.strptime(doc["dateTimeStart"], "%a %b %d %H:%M:%S %Y")
    unix=time.mktime(a.timetuple())
    return unix

runlist=[]

lines=abc_data.readlines()
for line in lines:
    val=line.strip("()\n").split(",")
    runid=int(float(val[0]))
    a=float(val[1])
    b=float(val[2])
    c=float(val[3])
    timer=find_time(runid)
    runlist.append((timer,a,b,c))
    


runlist.sort(key=lambda x:x[0])
print(runlist)
print(len(runlist))

   
canvas = ROOT.TCanvas("vil","AmBe MC", 850, 600)

#regularmc hist
h1= ROOT.TH2D("h1",'h1',100,runlist[0][0]-1000,runlist[-1][0]+1000,100,6500,7200)
h1.SetTitle("Parameter B  vs time")

for run in runlist:
    h1.Fill(run[0],run[2])
    
h1.SetStats(0)
h1.GetXaxis().SetTimeDisplay(1)
h1.GetXaxis().SetLabelSize(0.03)
h1.GetXaxis().SetTimeFormat("%m/%Y")
h1.GetXaxis().SetTimeOffset(0, "gmt")
h1.GetYaxis().SetTitle(" B parameter ")


h1.Draw("colz")

 
canvas.Update()

canvas.SaveAs("Bparameter_vsTime_allruns.png")

# this takes the output of getbestruns_avg and interpolates B parameters for every Physics run
#dir runlist must be a dir that contains text files with runnumbers seperated by a comma
# the output is the proper B parameter for every run number labelled in the runlist dir

import glob
import ROOT
import numpy as np
from  math import sqrt
import array
import re
import couchdb
import sys
import time
from datetime import datetime

dir_runlist="/home/trevorh/trevor_branch/data/highE_dataset/runlist/"
dir_output="/home/trevorh/trevor_branch/ambe_correction/final_go/official/"

abc_file="abc_official_interpolation_points_avg.txt"
output_file="abc_official_phys_runs.txt"


abc_data=open(dir_output+abc_file,"r")
lines=abc_data.readlines()

abc_runs={}
runlist=[]
for line in lines:
    val=line.strip("()\n").split(",")
    runid=int(float(val[0]))
    a=float(val[1])
    b=float(val[2])
    c=float(val[3])
    abc_runs[runid]=(a,b,c)
    runlist.append(runid)
   

    
def find_date(runid):
    server = couchdb.Server('https://deimos.physics.carleton.ca:6984')
    db = server['deapdb']
    ru_runer=runid
    docid = "RUNINFO_config_" + str(ru_runer) + "_" + str(ru_runer)
    doc = db[docid]
    a=doc["dateTimeStart"]
    runtime=datetime.strptime(doc["dateTimeStart"], "%a %b %d %H:%M:%S %Y")
    return runtime

def find_abc(runid):
    abc=abc_runs[runid]
    return abc        
            
def interpolate(r1,r2,target):
    
    a=find_date(r1)
    b=find_date(r2)
    c=find_date(target)
    delta = b - a
    delta_c=c-a
    diff=delta.days
    diff_c=delta_c.days
    
    
    if delta.days<2:
        abc=find_abc(r1)
        return abc

    ratio=diff_c/diff
    r1_abc=find_abc(r1)
    r2_abc=find_abc(r2)
    #linear interpolation
    abc=[0,0,0]
    
    for i in range(3):
        x=r2_abc[i]-r1_abc[i]     
        abc[i]=x/diff*diff_c+r1_abc[i]
        #print(abc[i])
    return abc
    
    
 


def find_best_abc(target_run):
    
    if target_run in abc_runs:
        abc=find_abc(target_run)
        return abc
    
    big=[]
    small=[]
    for run in runlist:
        if run>target_run:big.append(run)
        if run<target_run:small.append(run)
    
    
    if len(big)>0:
        r2=min(big)
        
    if len(small)>0:
        r1=max(small)
    
    
    if len(big)>0 and len(small)>0: abc=interpolate(r1,r2,target_run)
    elif len(big)>0:abc=find_abc(r2)
    elif len(small)>0:abc=find_abc(r1)
    
    return abc
        
out_txt=open(dir_output+output_file,"w")
input_files=glob.glob(dir_runlist+"*.txt")
for files in input_files:
    print("Starting runs from : ",files)
    f=open(files,"r")
    file_content=f.read()
    runs=file_content.split(",")
    for r in runs:
        abc=find_best_abc(int(r))
        out_txt.write(str((int(r),abc[0],abc[1],abc[2]))+"\n")
        
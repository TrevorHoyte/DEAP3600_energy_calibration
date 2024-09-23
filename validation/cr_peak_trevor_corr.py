#This file replots the AmBe data now with trevors energy correction and then outputs a txt file with thte Cr peak
#location for each run. and a pdf with the fits
# dir_data needs to hold the AmBe data with each run named in a root file run####.root eg run20714.root
# ABC file is a fiel containing the time dependent B paramters calculated earlier
#
# 
# 
# 
# format of csvfile
#make a while loop sigma on gaus bigger then 900 scanvas.SaveAs(dir_output+"%s_fit_gaus.png"%name)et tighter constraints
#runid,Date(YYYY,Month,Day),Cr peak mean,sigma, Shoulder exponential
import glob
import ROOT
import numpy as np
from  math import sqrt
import  array
import re

dir_output="/home/trevorh/trevor_branch/ambe_correction/compare_strategies/"
dir_data="/scratch/trevorh/data/AmBe_November2016ToMarch2020_L2/jobOutput/skimsum/"
abcfile="/home/trevorh/trevor_branch/ambe_correction/final_go/official/abc_official_phys_runs.txt"

plotFileName=dir_output+"Cr_fits_plots.pdf"



err_out=open(dir_output+"cr_peak_error.txt","w")
input_files=glob.glob(dir_data+"run*.root")

#ROOT.fStyle.chooseDSPalette(1)
canvas = ROOT.TCanvas()
canvas.SetLogy(1)
canvas.Print(plotFileName+"[")

binsize=0.060
MinBin = 1.5
MaxBin = 12
numbins=int((MaxBin-MinBin)/binsize)

cr_range=(9.45,9.85)

color=ROOT.kBlack
cuts="(qPE>10000 && fprompt>0.1 && fprompt<0.35 && fmaxpe<0.2 && deltat>20000 && numEarlyPulses<=3 && 2250 < eventTime && eventTime < 2700 && !(calcut & 0x31f8) && !(dtmTrigSrc & 0x82))"

def makehist(tree,name,abc):
    A=abc[0]
    B=abc[1]
    C=abc[2]
    
    h1 = ROOT.TH1F(name, "%s;energy MeV"%name, numbins, MinBin, MaxBin)
    h1.SetLineColor(color)
    tree.Draw("(-%s+sqrt(%s*%s-4*%s*(%s-qPE)))/(2*%s)>>"%(B,B,B,A,C,A)+name, cuts, "")
    h1 = ROOT.gDirectory.Get(name)
    #canvas.SaveAs(dir_output+"%s_full_qPE_Spectrum_image.png"%name)
    canvas.Print(plotFileName)
    
def make_zoomedhist(tree,name,peak,crrange,abc): 
    A=abc[0]
    B=abc[1]
    C=abc[2]
    name_zoom=name+peak
    h2 = ROOT.TH1F(name_zoom, "%s;energy MeV"%name_zoom, 100,crrange[0]-0.5,crrange[1]+0.5)
    h2.SetLineColor(color)
    h2.SetStats(0)
    tree.Draw("(-%s+sqrt(%s*%s-4*%s*(%s-qPE)))/(2*%s)>>"%(B,B,B,A,C,A)+name_zoom, cuts, "")
    h2 = ROOT.gDirectory.Get(name_zoom)
    events=h2.Integral()
    h2.Scale(1/events)
    #canvas.Print(plotFileName)
    return h2

#fitrange=64k-69k
def makefit_gauss(h):
   
    start_point=cr_range[1]
    window_size=0.4
    end_point=cr_range[0]
    increment=0.1
    
    mean=0
    mean_error=9e9
    best_iteration=0
    
    
    for i in range(int((start_point-end_point)/increment)+1):
        p1=start_point-(i)*increment
        p2=start_point+window_size-(i)*increment
        h.Fit("gaus","V","E1",p1,p2)
        h.Draw()
        gfit=h.GetFunction("gaus")
        mean_iter=gfit.GetParameter(1)
        mean_error_iter=gfit.GetParError(1)
        #canvas.SaveAs(dir_output+"%s_%sfit_gaus.png"%(name,i))
        if p1<mean_iter<p2 and mean_error_iter<mean_error:
            mean_error=mean_error_iter
            best_iteration=i
    
    #print best Iteration
    p1=start_point-(best_iteration)*increment
    p2=start_point+window_size-(best_iteration)*increment
    h.Fit("gaus","V","E1",p1,p2)
    h.Draw("qPE")
    gfit=h.GetFunction("gaus")
    
    gaus_mean=gfit.GetParameter(1)
    gaus_mean_err=gfit.GetParError(1)
    gaus_sigma=gfit.GetParameter(2)
    print("mean %s , and error : %s and sigma: %s ,"%(gaus_mean,gaus_mean_err,gaus_sigma))
    
    canvas.Print(plotFileName)
    
    values=(gaus_mean,gaus_mean_err,gaus_sigma)
    return values
    


#first tag abc for all the runs
files=open(abcfile)
linos=files.readlines()
dict_abc={}
for linee in linos:
    linee_info=linee.strip("()\n").split(",")
    dict_abc[int(float(linee_info[0]))]=(float(linee_info[1]),float(linee_info[2]),float(linee_info[3]))


    
#loop through all files:
cr_error=[]
kj=0
for file in input_files:
    kj+=1
    #if kj>2: break
    #open files to draw
    if file=='/scratch/trevorh/data/AmBe_November2016ToMarch2020_L2/jobOutput/skimsum/run26364.root':continue
    name=file.split("/")[-1].replace(".root","")
    n=re.findall(r'\d+', name)
    runid=int(n[0])
    #check if files good amberuns
    
    print("\n\n\n\n starting file:"+file)

    ambe_data=ROOT.TFile(file)
    tree=ambe_data.Get("data_satCorr")
    run_abc=dict_abc[runid]
    
    
    makehist(tree,name,run_abc)
    h=make_zoomedhist(tree,name,"Cr",cr_range,run_abc)
    result=makefit_gauss(h)
    cr_error.append((runid,result))
         
    
    #except:
    #print("this file failed to work: "+file)
    #err_out.write(name+"\n")

cr_error.sort(key=lambda x:abs(9.718-x[1][0]))
for item in cr_error:
    err_out.write(str(item)+"\n")

err_out.close()
canvas.Print(plotFileName +"]")


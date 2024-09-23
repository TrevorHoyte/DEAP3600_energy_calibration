# by trevor HOyte
# this code is used to fit Neutron capture peaks to Ambe spectrum
#first change the dir_output vairable to your desired locaytion where all output files will go
#dir_data contains a directory with all your amBe runs each run should be labelled as run####.root eg run20714.root
# this code will output a root file  ambe_ALl_fits.root that contains the information of each peak variable names are shown around line 28,
# it will also output a pdf with each run and each gaussian fit to each peak, finally it will output a error.txt file that has run numbers that failed.




import glob
import ROOT
import numpy as np
from  math import sqrt
import  array
import re

dir_output="/home/trevorh/trevor_branch/ambe_correction/multipeak/out/"
dir_data="/scratch/trevorh/data/AmBe_November2016ToMarch2020_L2/jobOutput/skimsum/"

plotFileName=dir_output+"ambefits_plots.pdf"
root_file=dir_output+"ambe_All_fits.root"

err_out=open(dir_output+"runs_error.txt","w")

input_files=glob.glob(dir_data+"run*.root")

#make rootfile
varnames = ["runid","Cr_mean","Cr_error","Cr_sigma","Fe_mean","Fe_error","Fe_sigma",
            "Sg_mean","Sg_error","Sg_sigma","H_mean","H_error","H_sigma",
            "crmaj_mean","crmaj_error","crmaj_sigma","crminor_mean","crminor_error","crminor_sigma",
            "ofear_mean","ofear_error","ofear_sigma"]
fout = ROOT.TFile(root_file, "RECREATE")
fout.cd()
output_tuple = ROOT.TNtuple("data","data",":".join(varnames))


#ROOT.fStyle.chooseDSPalette(1)
canvas = ROOT.TCanvas()
canvas.SetLogy(1)
canvas.Print(plotFileName+"[")

binsize=100
MinBin = 13000
MaxBin = 120000
numbins=int((MaxBin-MinBin)/binsize)

Cr_range=(62000,68000)
Fe_range=(49000,55000)
Sg_range=(27000,32000)
H_range=(13000,20000,"sharp")

cr_far=(59000,61500)
cr_close=(56000,59000)
o_fe=(40000,44000)

peaklist=["Cr","Fe","Sg","H","Cr_Ni_major","Cr_Ni_minor","O_FE_Ar"]
rangelist=[Cr_range,Fe_range,Sg_range,H_range,cr_far,cr_close,o_fe]

rangelist_alt=[(62000,66000),Fe_range,Sg_range,(13000,18000),cr_far,cr_close,o_fe]

color=ROOT.kBlack
cuts="(qPE>10000 && fprompt>0.1 && fprompt<0.35 && fmaxpe<0.2 && deltat>20000 && numEarlyPulses<=3 && 2250 < eventTime && eventTime < 2700 && !(calcut & 0x31f8) && !(dtmTrigSrc & 0x82))"

def makehist(tree,name):
    mothertree=tree
    h1 = ROOT.TH1F(name, "%s;energy MeV"%name, numbins, MinBin, MaxBin)
    h1.SetLineColor(color)
    mothertree.Draw("qPE>>"+name, cuts, "")
    h1 = ROOT.gDirectory.Get(name)
    #canvas.SaveAs(dir_output+"%s_full_qPE_Spectrum_image.png"%name)
    canvas.Print(plotFileName)
    
def make_zoomedhist(tree,name,peak,range): 
    name_zoom=name+peak
    h2 = ROOT.TH1F(name_zoom, "%s;energy MeV"%name_zoom, 150,range[0]-500,range[1]+500)
    h2.SetLineColor(color)
    h2.SetStats(0)
    tree.Draw("qPE>>"+name_zoom, cuts, "")
    h2 = ROOT.gDirectory.Get(name_zoom)
    events=h2.Integral()
    h2.Scale(1/events)
    #canvas.Print(plotFileName)
    return h2

#fitrange=64k-69k
def makefit_gauss(h,qpe_range):
   
    start_point=qpe_range[1]
    window_size=2000
    end_point=qpe_range[0]
    increment=500
    if len(qpe_range)>2:
        window_size=1000
    
    mean=0
    mean_error=9e9
    best_iteration=0
    
    
    for i in range(int((start_point-end_point)/increment)+1):
        p1=start_point-(i)*increment
        p2=start_point+window_size-(i)*increment
        h.Fit("gaus","V","E1",p1,p2)
        h.Draw("qPE")
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
    
 
#open erro files



#loop through all files:
#z=0
for file in input_files:
    #z+=1
    #if z>3:break
    print("\n\n\n\n starting file:"+file)
    ambe_data=ROOT.TFile(file)
    tree=ambe_data.Get("data_satCorr")
    name=file.split("/")[-1].replace(".root","")
    n=re.findall(r'\d+', name)
    runid=int(n[0])
    
    rangers=rangelist
    makehist(tree,name)
    
    fillvalues=[runid]
    try:
        for i in range(len(peaklist)):
            h=make_zoomedhist(tree,name,peaklist[i],rangers[i])
            result=makefit_gauss(h,rangers[i])
            for item in result:
                fillvalues.append(item)
                
        output_tuple.Fill(array.array("f",fillvalues))
    except:
        print("this file failed to work: "+file)
        err_out.write(name+"\n")



# write the tuple to the output file and close it
fout.cd()
output_tuple.Write()
err_out.close()
canvas.Print(plotFileName +"]")



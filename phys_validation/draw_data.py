#need to chnage the parameter B listed in lines 16- to 19 to corespond th the B parameters yourve created by interpolating
#make sure the ambe runs your are interested in are in dir data and have the nomenclature deap_ntp_highE*.root
import ROOT
import numpy
import array 
import glob
import math
import re
from ROOT import gROOT

dir_output="/home/trevorh/trevor_branch/ambe_correction/sambu/"
dir_data="/home/trevorh/data/phys/"

input_files=glob.glob(dir_data+"deap_ntp_highE*.root")

B_18950=7018.001237324859
B_19558=6942.262394302911
B_19862=6901.638833045684
B_20408=6841.047758628125
runlist=[(18950,B_18950,ROOT.kRed),(19558,B_19558,ROOT.kBlue),(19862,B_19862,ROOT.kBlack),(20408,B_20408,ROOT.kGreen)]

binsize=0.0603
MinBin = 1.5
MaxBin = 12
numbins=int((MaxBin-MinBin)/binsize)
cuts="(qPE>10000 && fprompt>0.1 && fprompt<0.35 && fmaxpe<0.2 && deltat>20000 && numEarlyPulses<=3 && 2250 < eventTime && eventTime < 2700 && !(calcut & 0x31f8) && !(dtmTrigSrc & 0x82))"

hs=ROOT.THStack("hs","Phys Comparisons with trevor correction; Energy (MeV)")
leg = ROOT.TLegend(0.85, 0.64, 0.65, 0.85)
leg.SetTextSize(0.03)
canvas = ROOT.TCanvas()
canvas.SetLogy(1)

A = -19.5064#   // PE / MeVee^2
#B = 6853.7#;     // PE / MeVee
C = 548.733#;    // PE
#LY = 7.126#.; 

def draw_hist(tree,name,B,color):
    mothertree=tree
    h1 = ROOT.TH1F(name, "%s;energy MeV"%name, numbins, MinBin, MaxBin)
    h1.SetLineColor(color)
    mothertree.Draw("(-%s+sqrt(%s*%s-4*%s*(%s-qPE)))/(2*%s)>>"%(B,B,B,A,C,A)+name, cuts, "")
    h1.SetStats(0)
    events=h1.Integral()
    h1.Scale(1/events)
    
    gROOT.cd()
    hnew = h1.Clone()
    hnew.Draw("hist")
    canvas.Update()
    canvas.SaveAs(name+".png")
    
    hs.Add(hnew)
    leg.AddEntry(hnew,name,"l")



for item in runlist:
    run=item[0]
    lycorr=float(item[1])
    color=item[2]
    
    for file in input_files:
        namer=file.split("/")[-1].replace(".root","")
        n=re.findall(r'\d+', namer)
        runid=int(n[0])
        if runid==int(run):
            print("\n\n\n\n starting file:"+file)
            ambe_data=ROOT.TFile(file)
            tree=ambe_data.Get("data_satCorr")
            draw_hist(tree,"run"+str(run),lycorr,color)
            break

    
    
    

hs.Draw("nostack")
leg.Draw()
canvas.Update()
canvas.SaveAs("phys_trevorcorr_sambu.png")
    
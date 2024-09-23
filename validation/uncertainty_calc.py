# uses the txt file output from  the cr_peak_trevor_corr.py file to fit a gaussian to the cr peak residyuuals.


import ROOT


dir_data="/home/trevorh/trevor_branch/ambe_correction/compare_strategies/out/"
peak_file="cr_peak_error_trevor.txt"
name_offix="trevor fix"

plotFileName=dir_data+"trevor_corr_uncertainty.pdf"



#ROOT.fStyle.chooseDSPalette(1)
canvas = ROOT.TCanvas()
canvas.SetLogy(1)
canvas.Print(plotFileName+"[")

binsize=0.060
MinBin = -0.2
MaxBin = 0.2
numbins=100

h1 = ROOT.TH1F("h1", "Cr_peak residual %s ;energy MeV"%name_offix, numbins, MinBin, MaxBin)
h1.SetLineColor(ROOT.kBlack)

energy_range=(-0.3,0.3)
def makefit_gauss(h):
   
    start_point=energy_range[0]
    end_point=energy_range[1]
  
    
    h.Fit("gaus","V","E1",start_point,end_point)
    h.Draw()
    gfit=h.GetFunction("gaus")
    gaus_mean=gfit.GetParameter(1)
    gaus_mean_err=gfit.GetParError(1)
    gaus_sigma=gfit.GetParameter(2)
    print("mean %s , and error : %s and sigma: %s ,"%(gaus_mean,gaus_mean_err,gaus_sigma))
    
    canvas.Print(plotFileName)
    
    values=(gaus_mean,gaus_mean_err,gaus_sigma)
    return values

#open 
file_loc=open(dir_data+peak_file,"r")
lines=file_loc.readlines()
for line in lines:
    line_info=line.strip("()\n").replace("(","").replace(")","").split(",")
    #print(line_info)
    peak=float(line_info[1])-9.718
    #print(peak)
    h1.Fill(peak)

h1.Draw()
#canvas.Save
canvas.Update()
events=h1.Integral()
h1.Scale(1/events) 
canvas.Print(plotFileName)

fit=makefit_gauss(h1)
print(fit)
    
canvas.Print(plotFileName +"]")



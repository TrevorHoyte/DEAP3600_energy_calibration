# this file creates a Bparameter from fitting a quadratic function with carls parameters fixed at A and C,
# and allowing B to float using data obtained by the multipeak.py code
# make sure data_file points to the output of multipeak's root file.
#the output is a file with the parabolas parameters for each runid in a txt file

import ROOT
import numpy as np
import array 
from scipy.optimize import curve_fit

data_file="/home/trevorh/trevor_branch/ambe_correction/validation/official/ambe_All_fits.root"
out_file="/home/trevorh/trevor_branch/ambe_correction/testing/out/abc_a19_cfixed.txt"

peak_data=ROOT.TFile(data_file)

f=open(out_file,"w")

#p(energy,qpe)

def func(x, b, c):
    return -19.51*x*x + b* x+548


def findabc(points):

    x=[]
    y=[]

    for item in points:
        x.append(item[0])
        y.append(item[1])
        
        
    #sol=np.linalg.lstsq(a,b)
    
    sol = curve_fit(func, x, y, bounds=((6000), (7500)))
    #print(sol)
    A=-19.51
    B=sol[0][0]
    C=548
    #C=sol[0][2]
    
    #print(A,B,C)
    #print(res)
    return A,B,C
fill=[]
for r in peak_data.data:
    runid=r.runid
    cr=(9.718,r.Cr_mean)
    fe=(7.63118,r.Fe_mean)
    sg=(4.44,r.Sg_mean)
    H=(2.22,r.H_mean)
    
    cr_ni_minor=(8.52,r.crminor_mean)  #8.51Cr 51, Ni59 8.53
    cr_ni_major=(8.94,r.crmaj_mean) #cr54 8.884 Ni59 8.998  
    ofear=(6.067,r.ofear_mean) # Ar41 6.142 Fe5.992
    
    
    
    A,B,C=findabc((cr,fe,H,sg)) #cr_ni_major,cr_ni_minor,ofear))
    #if A>-5.001 or A<-24.999: continue # or runid in [21747,27363]:continue
    print(A,B,C)
    fill.append((runid,A,B,C))
    
fill.sort(key=lambda x:x[0])
for item in fill:
    f.write(str(item)+"\n") 
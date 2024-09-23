#run skim.py directory_with_run_ntps outputdir qpemin,fromptmin,fpromptmax,fmaxpe0.2
# python skim.py /project/6004969/data/v5.11.0/ntp/run026034 /home/trevorh/trevor_branch/data/output_skim qpemin,fpromptmin,fpromptmax,fmaxpe
#25000,0.1,1,0.5
#
import ROOT
import sys
import os

#find fiels associated with a run
dir_to_be_skimmed=sys.argv[1]
files_in_dir=os.listdir(dir_to_be_skimmed)


#
output_dir=sys.argv[2]

#lis of cuts(qpemin,fpromptmin,fpromptmax,fmaxpe)
cuts=sys.argv[3]
print(cuts)
cuts_list=cuts.split(",")  
qPE_min=float(cuts_list[0])
fprompt_min=float(cuts_list[1])
fprompt_max=float(cuts_list[2])
fmaxpe_max=float(cuts_list[3])


#counter=0
#skim each file
for rootfile in files_in_dir:
    #counter+=1
    #if counter>2:
    #    break
    skimmed_file="skim_"+str(rootfile)
    
    old= ROOT.TFile.Open(dir_to_be_skimmed+"/"+rootfile);  oldtree = old.Get("data");  nentries = oldtree.GetEntries();
    print(nentries)
    
    newfile=ROOT.TFile(output_dir+"/"+skimmed_file, "recreate"); newtree=oldtree.CloneTree(0);
    for event in range(nentries):
        oldtree.GetEntry(event)
        #print(oldtree.qPE)
        if oldtree.qPE>qPE_min: # and oldtree.fprompt > fprompt_min and oldtree.fprompt < fprompt_max and oldtree.fmaxpe<fmaxpe_max:
            newtree.Fill()
            print("found_event")
    newfile.cd()
    newtree.Print()
    newfile.Write()


	

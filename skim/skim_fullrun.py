
import os, argparse
##############################################################################################
#official cuts qpe>25k <0.1fprompt<0.4 fmaxpe<0.2
#submitted blind2018 open2020, and blind 2019
#python test_fullrun.py --wdir /home/trevorh/trevor_branch/data/opendata2019_l2/ --dDir /project/6004969/data/v5.11.0/ntp/ --runs /home/trevorh/trevor_branch/data/runlist_opendata2019l2.txt --cuts 25000,0.1,0.4,0.3
#for all directories please ensure they end in a back slash , eg --dDir /projects/0049/data/v5.1/ntp/
parser = argparse.ArgumentParser(description='Takes a list of data runs and calculates their total livetime')
parser.add_argument('--wdir', dest='workDir', type=str, required=True, help='Directory for the output makesure the directory ends with a slash eg /home/trevorh/documents/output/')
parser.add_argument('--dDir', dest='dataDir', type=str, required=True, help='Directory where the full ntuples of the runs you wish to check are stored')
parser.add_argument('--runs', dest='runlist', type=str, required=True, help='Runlist to check. a text file with runs separated by commas on one or more lines')
parser.add_argument('--cuts', dest='cutlist', type=str, required=True, help='need a list of cuts for the skim format: qPEmax,fprompt_min,fpromptmax,fmaxpe')
args = parser.parse_args()

runsfile=open(args.runlist,'r')

runIDs=runsfile.read().split(',')

#print(runIDs)


#create directories
sub = args.workDir + 'submissionScripts/'
if not os.path.exists(sub): os.mkdir(sub)

out = args.workDir + 'jobOutput/'
if not os.path.exists(out): os.mkdir(out)
for id in runIDs:
    if not os.path.exists(out+"run"+id.strip()): os.mkdir(out+"run"+id.strip())


err = args.workDir + 'jobError/'
if not os.path.exists(err): os.mkdir(err)
for id in runIDs:
    if not os.path.exists(err+"run"+id.strip()):os.mkdir(err+"run"+id.strip())
    

#create submissions
    
for j in xrange(len(runIDs)):
	qFout  = open('%s/skimruns_%s.sh'%(sub, int(runIDs[j])), 'w+')
	qFout.write('''#!/bin/bash
#SBATCH --job-name skim_%s
#SBATCH --account=rrg-deap
#SBATCH --time 06:00:00
#SBATCH --mem=4096M
#SBATCH --output=%s
#SBATCH --error=%s
SRCDIR=%s
source /project/6004969/software/ratcage/env.sh
cd /home/trevorh/trevor_branch/data
python skim.py %s %s %s'''%(int(runIDs[j]), 
                            out+'run'+runIDs[j].strip()+'/' + '%x-%j.out',
                            err + 'run'+runIDs[j].strip()+'/''%x-%j.err',
                            args.workDir,
                            args.dataDir+"run0"+runIDs[j].strip(),
                            out+'run'+runIDs[j].strip(), 
                            args.cutlist ))
	qFout.close()

for file in sorted(os.listdir(sub)):
    #print(file)
    for w in xrange(len(runIDs)):
        if runIDs[w].strip() in file:
            fileFull = sub  + file
            #print(fileFull)
            os.system('sbatch %s'%fileFull)

# python skim.py /project/6004969/data/v5.11.0/ntp/run026034 /home/trevorh/trevor_branch/data/output_skim qpemin,fpromptmin,fpromptmax,fmaxpe

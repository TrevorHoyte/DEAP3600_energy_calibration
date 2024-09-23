#python adder.py --sdir ~/trevor_branch/data/opendata2019_l2/jobOutput/ --t opendata2019l2_ntp_skim
##makes a new directory called skimsum 
#python adder.py --sdir ~/trevor_branch/data/blinddata2018l2/jobOutput/ --t blinddata2018l2_ntp_skim
#python adder.py --sdir ~/trevor_branch/data/blinddata2019l2/jobOutput/ --t blinddata2019l2_ntp_skim
#python adder.py --sdir ~/trevor_branch/data/opendata2020_l2/jobOutput/ --t  opendata2020_ntp_skim
#python adder.py --ssdir ~/trevor_branch/data/ --t open

import os, argparse
parser = argparse.ArgumentParser(description='adds skimmed  data runs int one file')
parser.add_argument('--sdir', dest='sourcedir', type=str, required=True, help='Directory for the input root files eg /home/trevorh/documents/output/')
parser.add_argument('--t', dest='target', type=str, required=True, help='name of target file made in the source dir')
args = parser.parse_args()

sdir=args.sourcedir
tfile=args.target.strip()
#list of subdir
subdirs = [os.path.join(sdir, o) for o in os.listdir(sdir) if os.path.isdir(os.path.join(sdir,o))]

sum_dir=sdir+"skimsum"
if not os.path.exists(sdir+"skimsum"):os.mkdir(sum_dir)

#sums each subdir
for dir in subdirs:
    runsum=dir.split("/")[-1]
    print("adding NTP from: " + runsum)
    os.system('hadd %s/%s.root %s/*.root' %(sum_dir,runsum,dir))

#summ total in sum skim
os.system('hadd %s/%s.root %s/*.root' %(sum_dir,tfile,sum_dir))

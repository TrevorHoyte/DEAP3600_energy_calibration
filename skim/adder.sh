#!/bin/bash
#SBATCH --job-name add_alot_of_ntp
#SBATCH --account=rrg-deap
#SBATCH --time 01:00:00
#SBATCH --mem=4096M

source /project/6004969/software/ratcage/env.sh
cd /home/trevorh/trevor_branch/data
python adder.py --sdir ~/trevor_branch/data/nov2016Todec2017/jobOutput/ --t novToDec2017l2_ntp_skim

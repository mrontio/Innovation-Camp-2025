#!/bin/bash

#SBATCH --partition=<partition-name>
#SBATCH --nodes=<num-nodes>
#SBATCH --gres=gpu:<num-gpus>
#SBATCH --cpus-per-task=<cpus-per-task>
#SBATCH --time=00:00:00
#SBATCH --job-name=<job-name>
#SBATCH --output=run.out
#SBATCH --error=run.err
#SBATCH --reservation=<root>

######################################################################
module load conda/python3
module load cuda/12.4.0
source activate ic25
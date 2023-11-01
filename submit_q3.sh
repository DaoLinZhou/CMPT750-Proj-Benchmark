#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=5:00
#SBATCH --mem=4G
srun python3 launch_q3.py 8

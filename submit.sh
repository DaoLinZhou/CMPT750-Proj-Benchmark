#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=5:00
#SBATCH --mem=4G

export M5_PATH=/data/home/jiatangz/CMPT750-Proj

srun python3 launch.py 8

#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=5:00
#SBATCH --mem=4G
export M5_PATH=/home/ubuntu/Ass-1/gem5-baseline
export LAB_PATH=/home/ubuntu/Ass-1
srun python3 launch_q2.py 8

#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=120:00
#SBATCH --mem=40G

export PROJ_PATH=/data/home/rwa116/Project/CMPT750-Proj
export SPEC_PATH=/data/home/rwa116/Project/spec/benchspec/CPU
export BENCH_PATH=/data/home/rwa116/Project/CMPT750-Proj-Benchmark

# srun python3 launch.py 8
# srun python3 plots/plot4k.py 8
# srun python3 plots/plot64k.py 8
# srun python3 plots/line_chart.py 8
srun python3 plots/plotWeight.py 8

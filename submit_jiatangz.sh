#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=60:00
#SBATCH --mem=20G

export PROJ_PATH=/data/home/jiatangz/CMPT750-Proj
export SPEC_PATH=/data/home/jiatangz/spec2017/benchspec/CPU
export BENCH_PATH=/data/home/jiatangz/CMPT750-Proj-Benchmark

srun python3 launch.py 8

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

if not os.getenv("BENCH_PATH"):
    print("Set Bench Path\n")
    exit(1)


datadir = os.getenv('BENCH_PATH')+'/results/X86/spec2017'

def gem5GetStat(filename, stat):
    filename = os.path.join(datadir, '', filename, 'stats.txt').replace('\\','/')
    with open(filename) as f:
        r = f.read()
        if len(r) < 10: return 0.0
        if (r.find(stat) != -1) :
            start = r.find(stat) + len(stat) + 1
            end = r.find('#', start)
            print(r[start:end])
            return float(r[start:end])
        else:
            return float(0.0)

all_gem5_cpus = ['DerivO3CPU']

benchmarks = ['600.perlbench_s', '602.gcc_s', '605.mcf_s', '625.x264_s', '641.leela_s']

branch_predictors = ['BiModeBP', 'LTAGE', 'PerceptronBP']




rows = []
for bm in benchmarks: 
    for cpu in all_gem5_cpus:
        for bp in branch_predictors:
            rows.append([bm,cpu, bp,
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp, 'system.cpu.numCycles'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp, 'sim_insts'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp, 'sim_ops'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp, 'sim_ticks')/1e9,
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp, 'host_op_rate'),

            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp,'system.cpu.iew.predictedNotTakenIncorrect'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp,'system.cpu.iew.predictedTakenIncorrect'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp,'system.cpu.branchPred.condPredicted'),
            gem5GetStat(datadir+"/"+bm+"/"+cpu+"/"+bp,'system.cpu.branchPred.condIncorrect'),
            ])

df = pd.DataFrame(rows, columns=['benchmark','cpu', 'predictor', 'cycles','instructions', 'Ops', 'Ticks','Host', 'predictedNotTakenIncorrect', 'predictedTakenIncorrect', 'condPredicted', 'condIncorrect'])
df['ipc'] = df['instructions']/df['cycles']
df['cpi']= 1/df['ipc']
print(df)

width = min(0.2, 1/len(branch_predictors))
start_point = np.arange(len(benchmarks))

stat = "ipc"
plt.figure(figsize=(12.8, 7.2))

for i, bp in enumerate(branch_predictors):
    info = df[bp == df['predictor']][stat]
    plt.bar(start_point + i*width, info, width=width, label=bp)


plt.xticks(start_point+(len(branch_predictors)//2)*width, benchmarks, rotation=10, ha='right')
plt.legend(loc='upper left', prop={'size': 8})
plt.title("Compare IPC")
plt.ylabel("IPC")
plt.savefig("figures/Compare_ipc.png")

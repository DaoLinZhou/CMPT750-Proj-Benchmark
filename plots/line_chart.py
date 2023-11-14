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



preds_4K = ['4K_BiModeBP', '4K_PerceptronBP_ghs-28_pts-146']
preds_8K = ['8K_BiModeBP', '8K_PerceptronBP_ghs-34_pts-240']
preds_16K = ['16K_BiModeBP', '16K_PerceptronBP_ghs-36_pts-455']
preds_32K = ['32K_BiModeBP', '32K_PerceptronBP_ghs-59_pts-555']
preds_64K = ['64K_BiModeBP', '64K_PerceptronBP_ghs-59_pts-1110']
branch_categories = [preds_4K, preds_8K, preds_16K, preds_32K, preds_64K]
cat_labels = ['4kB', '8kB', '16kB', '32kB', '64kB']




rows = []
for bm in benchmarks: 
    for cpu in all_gem5_cpus:
        for bc in branch_categories:
            for bp in bc:
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
df['missRate'] = df['condIncorrect'] / df['condPredicted']
df['accuracy'] = 1 - df['missRate']
print(df)

width = min(0.2, 1/len(branch_categories))
start_point = np.arange(len(benchmarks))


def plot_stat(branch_categories, stat, title, ylabel, image_name, *args, **kwargs):
    yticks = kwargs.get('yticks', None)
    harmonic_means_bi = [0] * len(branch_categories)
    harmonic_means_perc = [0] * len(branch_categories)
    plt.figure(figsize=(12.8, 7.2))

    # for i, bc in enumerate(branch_categories):
    #     print("bc = " + str(bc))
    #     for j, bp in enumerate(bc):
    #         info = df[bp == df['predictor']][stat]
    #         if j = 0:
    #             harmonic_means_bi[i] += 1/info.iloc[0]
    #         else:
    #             harmonic_means_perc[i] += 1/info.iloc[0]
    #     harmonic_means_bi[i] = len(bc)/harmonic_means_bi[i]
    #     harmonic_means_perc[i] = len(bc)/harmonic_means_perc[i]

    for i, bc in enumerate(branch_categories):
        for benchmark in benchmarks:
            for bp in bc:
                info = df[(df['predictor'] == bp) & (df['benchmark'] == benchmark)][stat]
                if 'BiModeBP' in bp:
                    harmonic_means_bi[i] += 1 / info.iloc[0]
                elif 'PerceptronBP' in bp:
                    harmonic_means_perc[i] += 1 / info.iloc[0]
        harmonic_means_bi[i] = len(benchmarks) / harmonic_means_bi[i]
        harmonic_means_perc[i] = len(benchmarks) / harmonic_means_perc[i]

    plt.plot(np.linspace(0, 4, len(branch_categories)), harmonic_means_bi, marker='o')
    plt.plot(np.linspace(0, 4, len(branch_categories)), harmonic_means_perc, marker='*')
    plt.xticks(range(len(cat_labels)), cat_labels)
    plt.legend(loc='lower left', prop={'size': 8})
    plt.title(title)
    if yticks is not None:
        plt.yticks(yticks)
        plt.grid(axis='y', linestyle='--')
    plt.ylabel(ylabel)
    plt.savefig("plots/figures/{image_name}".format(image_name=image_name), bbox_inches='tight')
    plt.clf()


plot_stat(branch_categories, stat="missRate", title="Compare Miss Rate (Lower is Better)", ylabel="Percent Mispredicted", image_name='Hardware_budget.png')
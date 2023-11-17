from run import gem5Run
import subprocess
import os
import re
import sys
from uuid import UUID
from itertools import starmap
from itertools import product
import multiprocessing as mp
import argparse

def worker(bm, cpu, bp, bm_options):

    # if(bm == "603.bwaves_s"):
    #     subprocess.run('ulimit -s unlimited', shell=True)
    os.chdir(os.path.join(os.getenv('SPEC_PATH'),bm,'run/run_base_refspeed_mytest-m64.0000'))
    run = gem5Run.createSERun(
        'microbench_tests',
        os.getenv('PROJ_PATH')+'/build/X86/gem5.opt',
        os.getenv('PROJ_PATH')+'/configs/example/se.py',
        os.getenv('BENCH_PATH')+'/results/100M/X86/spec2017/{}/{}/{}'.format(bm,cpu,bp.name),
        '--cpu-type={cpu}'.format(cpu=cpu),
        '--caches',
        '--l2cache',
        '--l1d_size=32kB',
        '--l1i_size=32kB',
        '--l2_size=512kB',
        '--bp-type={bp}'.format(bp=bp.bp_model),
        *bp.params,
        '--cmd={cmd}'.format(cmd=os.path.join(os.getenv('SPEC_PATH'),bm,'build/build_base_mytest-m64.0000',bm.split(".")[1])),
        '--options={options}'.format(options=bm_options[bm]),
        '--sys-clock=4GHz',
        '--warmup-insts=1000000',
        '--maxinsts=100000000',
        timeout = 7200
        )

    run.run()
    json = run.dumpsJson()
    print(json)

class BranchPredictorConfig:
    def __init__(self, name, bp_model, params=[]) -> None:
         self.name = name
         self.bp_model = bp_model
         self.params = params


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('N', action="store",
                      default=1, type=int,
                      help = """Number of cores used for simulation""")
    args  = parser.parse_args()

    cpu_types = ['DerivO3CPU']
    branch_predictors = [
        # BranchPredictorConfig(name='LTAGE', bp_model='LTAGE'),
        BranchPredictorConfig(name='1K_BiModeBP', bp_model='BiModeBP', params={
            '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=128),
            '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=128)
        }),
        BranchPredictorConfig(name='2K_BiModeBP', bp_model='BiModeBP', params={
            '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=512),
            '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=512)
        }),
        # BranchPredictorConfig(name='4K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=2048),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=2048)
        # }),
        # BranchPredictorConfig(name='8K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=8192),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=8192)
        # }),
        # BranchPredictorConfig(name='16K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=16384),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=16384)
        # }),
        # BranchPredictorConfig(name='32K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=32768),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=32768)
        # }),
        # BranchPredictorConfig(name='64K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=65536),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=65536)
        # }),
        # BranchPredictorConfig(name='128K_BiModeBP', bp_model='BiModeBP', params={
        #     '--param=system.cpu[:].branchPred.choicePredictorSize={choicePredictorSize}'.format(choicePredictorSize=131072),
        #     '--param=system.cpu[:].branchPred.globalPredictorSize={globalPredictorSize}'.format(globalPredictorSize=131072)
        # }),
        BranchPredictorConfig(name='1K_PerceptronBP_ghs-12_pts-85', bp_model='PerceptronBP', params=[
            '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=12),
            '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=85),
            '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
            '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
            '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 12 + 14))
        ]),
        BranchPredictorConfig(name='2K_PerceptronBP_ghs-22_pts-93', bp_model='PerceptronBP', params=[
            '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=22),
            '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=93),
            '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
            '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
            '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 22 + 14))
        ])
        # ,
        # BranchPredictorConfig(name='4K_PerceptronBP_ghs-28_pts-146', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=28),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=146),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 28 + 14))
        # ]),
        # BranchPredictorConfig(name='8K_PerceptronBP_ghs-34_pts-240', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=43),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=240),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 43 + 14))
        # ]),
        # BranchPredictorConfig(name='16K_PerceptronBP_ghs-36_pts-455', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=36),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=455),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 36 + 14))
        # ]),
        # BranchPredictorConfig(name='32K_PerceptronBP_ghs-59_pts-555', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=59),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=555),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93 * 59 + 14))
        # ]),
        # BranchPredictorConfig(name='64K_PerceptronBP_ghs-59_pts-1110', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=59),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=1110),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93*59+14))
        # ]),
        # BranchPredictorConfig(name='128K_PerceptronBP_ghs-62_pts-2114', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=62),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=2114),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<7)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<7)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93*62+14))
        # ]),
        # BranchPredictorConfig(name='64K_PerceptronBP_ghs-59_pts-1110_wgh-32', bp_model='PerceptronBP', params=[
        #     '--param=system.cpu[:].branchPred.globalHistorySize={globalHistorySize}'.format(globalHistorySize=59),
        #     '--param=system.cpu[:].branchPred.perceptronTableSize={perceptronTableSize}'.format(perceptronTableSize=1110),
        #     '--param=system.cpu[:].branchPred.maxWeight={maxWeight}'.format(maxWeight=(1<<31)-1),
        #     '--param=system.cpu[:].branchPred.minWeight={minWeight}'.format(minWeight=-(1<<31)),
        #     '--param=system.cpu[:].branchPred.threshold={threshold}'.format(threshold=int(1.93*59+14))
        # ])
    ]

    # All benchmarks must have full name hardcoded here
    # Executable file in build_base directory must be renamed in some cases to match the benchmark name (ex. gcc_s)
    bm_list = ['600.perlbench_s', '602.gcc_s', '605.mcf_s', '625.x264_s', '641.leela_s']

    # All reference inputs for spec benchmarks must be hardcoded in bm_options dictionary
    bm_options = {
        '600.perlbench_s': '-I./lib checkspam.pl 2500 5 25 11 150 1 1 1 1 > checkspam.2500.5.25.11.150.1.1.1.1.out 2>> checkspam.2500.5.25.11.150.1.1.1.1.err',
        '602.gcc_s': 'gcc-pp.c -O5 -fipa-pta -o gcc-pp.opts-O5_-fipa-pta.s > gcc-pp.opts-O5_-fipa-pta.out 2>> gcc-pp.opts-O5_-fipa-pta.err',
        '605.mcf_s': 'inp.in  > inp.out 2>> inp.err',
        '625.x264_s': '--pass 1 --stats x264_stats.log --bitrate 1000 --frames 1000 -o BuckBunny_New.264 BuckBunny.264 1280x720 > run_000-1000_x264_s_base.mytest-m64_x264_pass1.out 2>> run_000-1000_x264_s_base.mytest-m64_x264_pass1.err',
        '641.leela_s': 'ref.sgf > ref.out 2>> ref.err'
    }

    print(bm_list)

    jobs = []
    for bm in bm_list:
        for cpu in cpu_types:
                for bp in branch_predictors:
                    jobs.append((bm, cpu, bp, bm_options))

    with mp.Pool(args.N, maxtasksperchild=1) as pool:
        pool.starmap(worker,jobs)

# Test with 1 million instructions, find some threshold that limits the time for execution to 2 hours
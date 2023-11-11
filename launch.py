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
        os.getenv('BENCH_PATH')+'/results/X86/spec2017/{}/{}/{}'.format(bm,cpu,bp),
        '--cpu-type={cpu}'.format(cpu=cpu),
        '--bp-type={bp}'.format(bp=bp),
        '--cmd={cmd}'.format(cmd=os.path.join(os.getenv('SPEC_PATH'),bm,'build/build_base_mytest-m64.0000',bm.split(".")[1])),
        '--options={options}'.format(options=bm_options[bm]),
        '--sys-clock=4GHz',
        '--warmup-insts=1000000',
        '--maxinsts=10000000'
        )

    run.run()
    json = run.dumpsJson()
    print(json)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('N', action="store",
                      default=1, type=int,
                      help = """Number of cores used for simulation""")
    args  = parser.parse_args()

    cpu_types = ['TimingSimpleCPU']
    branch_predictors = ['LTAGE', 'PerceptronBP']

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
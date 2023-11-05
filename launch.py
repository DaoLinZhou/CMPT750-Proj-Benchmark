from run import gem5Run
import os
import re
import sys
from uuid import UUID
from itertools import starmap
from itertools import product
import multiprocessing as mp
import argparse

def worker(run):
    run.run()
    json = run.dumpsJson()
    print(json)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('N', action="store",
                      default=1, type=int,
                      help = """Number of cores used for simulation""")
    args  = parser.parse_args()

    # cpu_types = ['Simple','DefaultO3','Minor4', 'O3_W256', 'O3_W2K']
    cpu_types = ['DefaultO3']
    # mem_types = ['SingleCycle', 'Inf', 'Slow']
    mem_types = ['Slow']
    branch_predictors = ['LTAGE', 'AlwaysTakenBP', 'PerceptronBP']

    bm_list = []
    benchPattern = re.compile(r'^619')

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    dir_path = '/data/home/rwa116/Project/spec/benchspec/CPU'
    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        if os.path.isdir(full_path) and benchPattern.match(filename):
            bm_list.append(filename)
    print(bm_list)

    jobs = []
    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                for bp in branch_predictors:
                    run = gem5Run.createSERun(
                        'microbench_tests',
                        os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                        'gem5-config/run_micro.py',
                        'results/X86/run_micro/{}/{}/{}/{}'.format(bm,cpu,mem,bp),
                        cpu,mem,bp, os.path.join('/data/home/rwa116/Project/spec/benchspec/CPU',bm,'build/build_base_mytest-m64.0000',bm.split(".")[1]),
                        '')
                    jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker,jobs)


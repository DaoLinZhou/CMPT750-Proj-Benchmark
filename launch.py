from run import gem5Run
import os
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
    branch_predictors = ['LTAGE', 'PerceptronBP']

    bm_list = []

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    for filename in os.listdir('microbenchmark'):
        if os.path.isdir(f'microbenchmark/{filename}') and filename != '.git':
            bm_list.append(filename)

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
                        cpu,mem,bp, os.path.join('microbenchmark',bm,'bench.X86'))
                    jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker,jobs)


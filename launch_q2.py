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

    cpu_types = ['Simple', 'O3_W256']
    mem_types = ['Slow']
    L1_cache = ['4kB','8kB','32kB','64kB']
    L2_cache = ['128kB','256kB','512kB','1MB']

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
                for l1 in L1_cache:
                    for l2 in L2_cache:
                        run = gem5Run.createSERun(
                            'microbench_tests',
                            os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                            'gem5-config/run_micro_q2.py',
                            'results/X86/run_micro/q2/{}/{}/{}/{}/{}'.format(bm,cpu,mem,l1,l2),
                            cpu,mem, l1, l2, os.path.join('microbenchmark',bm,'bench.X86'))
                        jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker,jobs)


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

    cpu_types = ['Minor4']
    mem_types = ['Slow']
    DRAMs_q1 = ['DDR3_1600_8x8']
    clocks_q1 = ['1GHz', '2GHz']
    bm_list = []

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    for filename in os.listdir('microbenchmark_no_ROI'):
        if os.path.isdir(f'microbenchmark_no_ROI/{filename}') and filename != '.git':
            bm_list.append(filename)

    jobs = []
    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                for dram in DRAMs_q1:
                    for clock in clocks_q1:
                        run = gem5Run.createSERun(
                            'microbench_tests',
                            os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                            'gem5-config/run_micro_q4.py',
                            'results/X86/run_micro/q4/{}/{}/{}/{}/{}/'.format(bm,cpu,mem, dram, clock),
                            cpu,mem, dram, os.path.join('microbenchmark_no_ROI',bm,'bench.X86'), "--clock="+clock)
                        jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker,jobs)


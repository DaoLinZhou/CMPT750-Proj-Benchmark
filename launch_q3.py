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

    cpu_types = ['Simple', 'Minor4']
    mem_types = ['Slow']
    DRAMs_q1 = ['DDR3_1600_8x8']
    DRAMs_q2 = ['DDR3_2133_8x8', 'LPDDR2_S4_1066_1x32', 'HBM_1000_4H_1x64']
    clocks_q1 = ['1GHz', '2GHz', '4GHz']
    clocks_q2 = ['4GHz']
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
                for dram in DRAMs_q1:
                    for clock in clocks_q1:
                        run = gem5Run.createSERun(
                            'microbench_tests',
                            os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                            'gem5-config/run_micro_q3.py',
                            'results/X86/run_micro/q3/{}/{}/{}/{}/{}/'.format(bm,cpu,mem, dram, clock),
                            cpu,mem, dram, os.path.join('microbenchmark',bm,'bench.X86'), "--clock="+clock)
                        jobs.append(run)

    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                for dram in DRAMs_q2:
                    for clock in clocks_q2:
                        run = gem5Run.createSERun(
                            'microbench_tests',
                            os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                            'gem5-config/run_micro_q3.py',
                            'results/X86/run_micro/q3/{}/{}/{}/{}/{}/'.format(bm,cpu,mem, dram, clock),
                            cpu,mem, dram, os.path.join('microbenchmark',bm,'bench.X86'), "--clock="+clock)
                        jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker,jobs)


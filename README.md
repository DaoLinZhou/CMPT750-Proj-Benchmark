In addition to this benchmark repository: https://github.com/DaoLinZhou/CMPT750-Proj-Benchmark/tree/spec2017work, there are several files we have modified in the gem5 repository linked here: https://github.com/DaoLinZhou/CMPT750-Proj/tree/RandomForest including:
src/cpu/pred/BranchPredictor.py
src/cpu/pred/SConscript
src/cpu/pred/perceptron.cc
src/cpu/pred/perceptron.hh
src/cpu/pred/perceptronForest.cc
src/cpu/pred/perceptronForest.hh

To reproduce the results and plots seen in this repository and in our report, please follow these steps, OR the alternative option below:
1. In the CMPT750-Proj repository, run the build.sh script to build gem5 with our modifications.
2. In the CMPT750-Proj-Benchmark repository, run launch.py to run all benchmarks on all branch predictor configurations. WARNING: Running all of these at the same time could take upwards of 4 hours.
3. Run line_chart.py, plot4k.py, plot64k.py, plot128k.py, plotForestCompare.py, plotWeight.py, plotWeight4k.py to generate all plots

Alternatively, you can run the submit_rwa116.sh script to use a precompiled gem5 build and already generated statistics files to generate all new plots.


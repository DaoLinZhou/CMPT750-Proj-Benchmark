[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/A8b79HZz)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11754810&assignment_repo_type=AssignmentRepo)
## README

For each question, I wrote a script to generate the results.
Please check `launch_*.py` for details

You can simply run the commands below to get all the results
```shell
sbatch submit_q1.sh
sbatch submit_q2.sh
sbatch submit_q3.sh
sbatch submit_q4.sh
```

The output will be saved in 
```
$REPO/results/X86/run_micro/q1
$REPO/results/X86/run_micro/q2
$REPO/results/X86/run_micro/q3
$REPO/results/X86/run_micro/q4
```

> Each question also uses different run_micro_*.py, which is already specify in the script, 
> you don't need to do anything. you can check `$REPO/gem5-config/run_micro_*.py` if you are interested.

To generate the plot, please use following commands
```shell
cd $REPO          # go to the root of project folder

export LAB_PATH=$PWD
cd plots

# Plots for each question will be saved to different folder
mkdir q1 & mkdir q2 & mkdir q3 & mkdir q4

python3 scripts_q1.py
python3 scripts_q2.py
python3 scripts_q3.py
python3 scripts_q4.py
python3 scripts_q4_p2.py
```


Add more branch predictors under

1. Add the predictor name under ```launch.py: branch_predictors```
2. Add the predictor class under ```gem5-config/run_micro.py: valid_bps```


Submit the job using
```sbatch submit.sh```
> Don't forget to change the M5_PATH `export M5_PATH=/data/home/...` in `submit.sh`


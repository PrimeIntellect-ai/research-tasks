I am a researcher running parallelized Monte Carlo simulations to estimate Pi, but I am running into issues with a custom simulation package. 

I have a vendored MPI-based Python package called `montecarlo-pi-mpi` located at `/app/montecarlo-pi-mpi-1.0.0`. It contains a script `simulate.py` designed to be run with `mpi4py`. It distributes point sampling across MPI processes to estimate Pi. 

However, the package is broken. When I run `mpirun -n 4 python /app/montecarlo-pi-mpi-1.0.0/simulate.py --samples 100000`, the final estimated value of Pi is way off (usually around 1.0 instead of 3.14). There is a bug in how the MPI processes combine their local counts. 

Here is what I need you to do:
1. Identify and fix the bug in `/app/montecarlo-pi-mpi-1.0.0/simulate.py`. Note: This environment has no internet access, so you must fix the source code directly.
2. Write a Python orchestration script at `/home/user/run_experiment.py` that uses the `subprocess` module to repeatedly execute the fixed `simulate.py` script 50 times. Each execution should use `mpirun -n 4 python /app/montecarlo-pi-mpi-1.0.0/simulate.py --samples 10000 --seed <run_index>` (where run_index goes from 0 to 49).
3. Extract the estimated Pi value from the standard output of each run.
4. Using these 50 estimates, write a function to calculate the 95% bootstrap confidence interval of the mean of these estimates. Use exactly 10,000 bootstrap resamples and a random seed of 42 for the resampling process. Use the percentile method (2.5th and 97.5th percentiles).
5. Save the final results to `/home/user/bootstrap_results.json` with the following exact format:
```json
{
  "mean_estimate": 3.1415...,
  "ci_lower": 3.13...,
  "ci_upper": 3.15...
}
```

Ensure your bootstrap implementation accurately samples with replacement from your 50 observations.
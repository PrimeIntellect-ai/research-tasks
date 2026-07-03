You are an ML Engineer preparing training data for a neural network surrogate model. You have been provided with a legacy Bash-based Monte Carlo/MCMC sampling package located at `/app/mcmc-bash-pkg-1.0.tar.gz`.

Currently, the simulation tool produces non-reproducible results. When generating Monte Carlo chains, the mathematical reduction (an Exponential Moving Average) yields slightly different floating-point results every time it is run with the same seed. This is because the internal script launches parallel Bash background jobs that append their output to a shared file without synchronization, resulting in a randomized order of operations during the EMA reduction step.

Your task consists of the following steps:

1. **Extract and Fix the Package:**
   Extract the package into `/home/user/workspace/`. 
   Diagnose and patch the scripts inside the package. You must ensure that the Monte Carlo steps are processed by the aggregation step in strictly numerical sequence (from step 1 to `N_SAMPLES`) so that the floating-point reduction is deterministic and mathematically correct. 

2. **Parallel Data Generation:**
   Write a new Bash script at `/home/user/workspace/generate_dataset.sh`.
   This script must orchestrate the generation of our training dataset by running the fixed MCMC generator for exactly 100 different seeds, from `1000` to `1099` (inclusive).
   For each seed, you must generate `500` samples.
   To save time, your `generate_dataset.sh` script should distribute the work to run the seeds in parallel (e.g., using `xargs -P`, `wait`, or `GNU parallel`).

3. **Output Formatting:**
   Your `generate_dataset.sh` script must produce a final compiled CSV file at `/home/user/workspace/dataset.csv`.
   The file must contain exactly 100 lines (one for each seed).
   Each line must be formatted as: `seed,final_ema_value`
   The lines in `dataset.csv` must be sorted numerically by the seed value.

Execute your script to produce the final `dataset.csv` file. An automated test will evaluate the numerical accuracy of your generated EMAs against a reference implementation.
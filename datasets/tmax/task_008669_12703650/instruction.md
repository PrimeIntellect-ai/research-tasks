You are a researcher processing noisy velocity data from a series of 50 simulation runs. You need to calculate the total distance traveled in each simulation and estimate the 95% confidence interval of the mean distance using bootstrap resampling.

The raw data is located in the directory `/home/user/sim_data/`. There are 50 files named `sim_1.csv` through `sim_50.csv`. Each file has a header `t,v` representing time (seconds) and velocity (meters/second).

Your task is to write a single Bash pipeline script at `/home/user/pipeline.sh` that performs the following operations using **only** standard Linux command-line tools (bash, awk, bc, sort, etc.). **Do not use Python, R, Perl, or any other high-level scripting languages.**

The script must:
1. **Numerical Integration:** For each CSV file, calculate the total distance traveled using the **Trapezoidal Rule** to integrate `v` with respect to `t`. 
2. **Mean Calculation:** Calculate the mean of these 50 distances.
3. **Bootstrap Resampling:** Generate `B=10000` bootstrap samples (resampling the 50 distances with replacement). For each sample, calculate the mean distance. Use `awk`'s random number generator initialized with the seed `12345` (e.g., `awk -v seed=12345 'BEGIN{srand(seed)} ...'`).
4. **Confidence Interval:** Determine the 95% confidence interval by finding the 2.5th and 97.5th percentiles of your 10,000 bootstrap sample means.

Your script `/home/user/pipeline.sh` should execute these steps and save the final output to `/home/user/result.txt` in exactly this format:
```
Mean: <original_mean>
95% CI: [<lower_bound>, <upper_bound>]
```
(Format values to 3 decimal places).

Finally, run your script so that `/home/user/result.txt` is generated.
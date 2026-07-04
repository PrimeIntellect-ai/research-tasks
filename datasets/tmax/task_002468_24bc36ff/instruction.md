You are a performance engineer tasked with profiling and correcting a Bash-based data analysis pipeline. 

A previous engineer wrote a numerical integration script to calculate the total energy from 50 simulated experimental runs. The simulation output files are located in `/home/user/simulation_runs/` (named `run_1.csv` to `run_50.csv`). Each file contains two comma-separated columns: `time` and `energy`.

The current integration script at `/home/user/integrate.sh` computes the area under the curve using `awk`. However, it produces wildly incorrect and diverging results because it incorrectly assumes a constant time step (`dt = 0.1`). In reality, the simulation relies on an adaptive time-stepper, so the time steps vary.

Your tasks are as follows:

1. **Fix the Integrator**: Modify `/home/user/integrate.sh` to correctly compute the numerical integral using the **Trapezoidal Rule**. It must handle non-uniform time steps correctly. The script should take a single CSV file as an argument and print ONLY the final integrated value to standard output.

2. **Parallel Processing**: Use `xargs` to run your corrected `/home/user/integrate.sh` on all 50 CSV files in `/home/user/simulation_runs/` in parallel. You must configure `xargs` to use exactly **4 concurrent processes**. Save the output (50 numerical values, one per line) to `/home/user/all_integrals.txt`.

3. **Bootstrap Confidence Interval**: Write a new script `/home/user/bootstrap.sh` that reads `/home/user/all_integrals.txt` and calculates a 95% bootstrap confidence interval for the **mean** of these integrals.
   - You must generate exactly **1000** bootstrap resamples. 
   - Each resample should consist of 50 values drawn *with replacement* from the 50 integrals.
   - Calculate the mean of each resample.
   - Sort these 1000 means and extract the 95% confidence interval (the 2.5th percentile and 97.5th percentile, which correspond to the 25th and 975th values in the sorted list).
   - The script should output these two values separated by a comma (e.g., `124.53,126.12`) directly to `/home/user/ci.txt`.

Ensure all your scripts are executable. Use only standard bash built-ins and POSIX tools (like `awk`, `sort`, `sed`, `xargs`). Do not use Python, Perl, or R.
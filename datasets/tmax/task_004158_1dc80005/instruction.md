You are a performance engineer tasked with profiling a numerical simulation engine that relies on matrix decomposition. The simulation engine occasionally diverges due to numerical instabilities caused by inappropriate step sizes (`dt`).

Your tasks are:

1. **Compilation**: You will find the source code for the simulation engine at `/home/user/matrix_sim.c`. Compile it into an executable named `/home/user/matrix_sim` using `gcc` with the `-O2` and `-lm` flags.

2. **Profiling and Simulation**: Write a Bash script at `/home/user/profile.sh` that acts as a parameter sweeper. The script should:
   - Loop through step sizes (`dt`) from `0.010` to `0.100` inclusive, in increments of `0.001` (ensure exactly 3 decimal places are used).
   - For each `dt`, run the compiled `./matrix_sim <dt>`.
   - Capture the output of the simulation (which will be either "SUCCESS" or "DIVERGED").

3. **Data Reshaping**: As your script runs the simulations, it must reshape and record the observational data into a CSV file at `/home/user/results.csv`.
   - The format for each line must be exactly: `dt,status` (e.g., `0.055,SUCCESS` or `0.091,DIVERGED`).
   - Do not include a header row.

4. **Analysis**: Determine the maximum `dt` value (formatted to 3 decimal places) that results in a "SUCCESS" status. Save this single numeric value to `/home/user/optimal_dt.txt`.

Ensure your Bash script (`/home/user/profile.sh`) is executable and can be run to generate the required output files automatically.
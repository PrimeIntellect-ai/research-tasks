You are tasked with fixing a broken scientific computing pipeline for molecular simulations. The pipeline involves parsing a PDB file, performing a Monte Carlo convergence simulation in C, bootstrapping the results in Python, and running a regression test against a known baseline.

The project is located at `/home/user/protein/`.

Here are your instructions:
1. **Scientific Environment Management:** Install the GNU Scientific Library (`libgsl-dev`) which is required for the C program. You can use `sudo apt-get` (sudo is not required if running as root/admin in the environment, but assume standard package manager access). *Note: if you encounter permission issues, remember the container may allow apt-get without sudo.*
2. **Bioinformatics Format Parsing & Convergence Testing (C):** 
   - A skeleton file `/home/user/protein/simulate.c` exists. Update it to parse the provided PDB file `/home/user/protein/1xyz.pdb`.
   - Extract the `X, Y, Z` coordinates *only* for atoms where the atom name is exactly `CA` (Alpha Carbon).
   - Implement a Monte Carlo loop: use GSL's `gsl_rng_mt19937` seeded with the integer passed as the second command-line argument (`argv[2]`). Randomly pick two distinct `CA` atoms and compute their Euclidean distance. 
   - Keep a running sum to calculate the mean distance.
   - **Convergence Condition:** Every 100 iterations, calculate the mean of the *current block of 100 samples* and compare it to the mean of the *previous block of 100 samples*. If the absolute difference is less than `0.01`, the simulation has converged. Print the *overall* mean of all samples drawn so far to standard output and exit.
3. **Bootstrap Confidence Intervals & Regression Testing (Python):**
   - Write a script `/home/user/protein/test_pipeline.py`.
   - The script should compile `simulate.c` using `gcc -o simulate simulate.c -lgsl -lgslcblas -lm`.
   - Run `./simulate 1xyz.pdb <seed>` 50 times, using seeds 1 through 50, and collect the 50 converged means.
   - Calculate the 95% bootstrap confidence interval of these 50 means by performing 1000 resamples (with replacement). Use the 2.5th and 97.5th percentiles.
   - Read `/home/user/protein/baseline.txt`, which contains `Expected Mean: 8.169`. If the overall mean of your 50 collected means is within `0.2` of this expected mean, the regression test passes.
4. **Output Logging:**
   - Create `/home/user/protein/regression_report.log` with exactly this format:
     ```
     Overall Mean: <mean_rounded_to_3_decimals>
     95% CI: [<lower_rounded_to_3_decimals>, <upper_rounded_to_3_decimals>]
     Regression: <PASS|FAIL>
     ```

Make sure all scripts are executable and run correctly. Leave the final log file at `/home/user/protein/regression_report.log`.
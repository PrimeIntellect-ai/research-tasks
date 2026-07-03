You are a performance engineer tasked with profiling a scientific simulation and proving the statistical significance of compiler optimizations. 

A compute-heavy C++ scientific simulation is located at `/home/user/sim.cpp`. 

Your task is to:
1. **Compile**: Compile `/home/user/sim.cpp` into two separate executables using `g++`:
   - `/home/user/sim_o2` compiled with `-O2`
   - `/home/user/sim_o3` compiled with `-O3 -ffast-math`

2. **Regression Testing**: Both executables must produce exactly the same scientific result. When run, the simulation prints its final computed state on the first line of standard output, and its execution time on the second line (e.g., `Time: 142.5 ms`). Run a regression test to ensure the first line of output is strictly identical between the two binaries.

3. **Profiling**: Run each binary 50 times. Extract the execution time from the second line of the output for each run.

4. **Statistical Analysis**: Set up a software environment (using any language/tools you prefer) and write a script to compute the 95% Bootstrap confidence interval of the *difference in mean execution times* between the two binaries (`mean(O2_times) - mean(O3_times)`). 
   - Use the percentile method for the bootstrap.
   - Use exactly 10,000 resamples.
   - Use a fixed random seed of `42` for your bootstrap resampling to ensure reproducibility.

5. **Reporting**: Create a JSON file at `/home/user/profile_report.json` with exactly the following format:
```json
{
  "regression_passed": true,
  "mean_diff": 15.2,
  "ci_lower": 12.1,
  "ci_upper": 18.5
}
```
*Note: The values above are just examples. Ensure your types match (boolean for regression, floats for the rest).*

All scripts and binaries should be self-contained in `/home/user/`. Do not require root access.
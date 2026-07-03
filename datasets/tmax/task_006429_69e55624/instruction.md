You are a performance engineer analyzing a diverging numerical integrator used for primer design and sequence alignment kinetics. The simulation frequently diverges due to wrong step-size adaptation, producing `NaN` or `Inf` error values. 

You have been given a messy observational log file located at `/home/user/integration_logs.txt`. 
The file contains interleaved logs from 50 different simulation runs. The format of each line is:
`[RunID=<ID>] step=<step_num> size=<step_size> error=<error_value>`

Your task is to:
1. **Reshape and Clean the Data:** Extract the maximum error value achieved in each `RunID`. However, if a `RunID` contains *any* step with an error of `NaN` or `Inf`, you must completely exclude that `RunID` from your analysis (the entire run is considered diverged). 
2. **Compute Bootstrap Confidence Intervals:** Write a Python script to calculate the 95% bootstrap confidence interval for the *mean* of these maximum error values across all valid runs.
   - Use exactly `10000` bootstrap iterations.
   - Resample with replacement. The sample size for each bootstrap iteration must equal the number of valid runs.
   - Use `numpy` for calculations. Set `numpy.random.seed(42)` immediately before your bootstrap loop.
   - Use `numpy.percentile` to extract the 2.5th and 97.5th percentiles from your array of bootstrapped means.
3. **Save Results:** Write the final confidence interval to a file named `/home/user/ci_results.txt` in exactly the following format (rounded to 5 decimal places):
   `Lower: X.XXXXX, Upper: Y.XXXXX`

You may use standard Linux shell tools (like `awk`, `grep`, `sort`) and Python to accomplish this. Ensure your final output is exactly as requested.
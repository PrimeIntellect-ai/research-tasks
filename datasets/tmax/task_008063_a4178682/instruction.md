You are assisting a data scientist in debugging a numerical integrator that diverged due to poor step-size adaptation. You have been provided with a CSV log file at `/home/user/integrator.csv` containing the columns: `step,time,value,residual`.

Because the environment is minimal, you must use standard bash tools (e.g., `awk`, `grep`, `sed`, `bc`, `coreutils`) to analyze the high-frequency oscillations in the residuals.

Write a reproducible bash script at `/home/user/analyze.sh` that performs the following tasks:
1. Calculates the "zero-crossing rate" of the `residual` column. This acts as a rudimentary spectral analysis of the divergence frequency. A zero-crossing occurs when the sign of the residual strictly changes between consecutive rows (i.e., the product of consecutive residuals is strictly less than 0). The rate is defined as `(number of zero crossings) / (N - 1)`, where `N` is the total number of residual values.
2. Computes a coarse density estimation (histogram counts) of all residuals into three bins:
   - `Negative`: residual < -1.0
   - `Neutral`: -1.0 <= residual <= 1.0
   - `Positive`: residual > 1.0
3. Prints the results to standard output in exactly the following format (round the rate to 4 decimal places):

```
Zero-crossing rate: 0.XXXX
Negative: X
Neutral: X
Positive: X
```

Once you have created `/home/user/analyze.sh`, ensure it is executable, run it, and redirect its output to `/home/user/report.txt`.
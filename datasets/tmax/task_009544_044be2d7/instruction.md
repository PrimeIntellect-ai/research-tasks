You are a performance engineer profiling a scientific application. You have been given a set of execution logs from a distributed network simulator. Your goal is to analyze the asymptotic time complexity of a specific function, `ComputeEigen`, to validate if its implementation matches the expected analytical analytical scaling behavior and if the numerical performance is stable.

In `/home/user/profiling_data/`, there are several CSV files named `run_N<size>.csv`, where `<size>` is the input graph size (N). Each file contains profiling data with the format:
`Function,Caller,ExecutionTime_ms`

Your task is to write a purely Bash/AWK-based analysis pipeline (no Python, R, or Perl) that does the following:
1. Extracts the total execution time (summing the `ExecutionTime_ms` column) spent in the `ComputeEigen` function for each input size N.
2. Performs a linear regression on the log-log scale of the data (i.e., $x = \ln(N)$, $y = \ln(T)$) to find the empirical scaling exponent (the slope of the regression line).
3. Validates the analytical solution: The theoretical time complexity of this algorithm is $O(N^3)$. If the calculated slope is between 2.90 and 3.10 (inclusive), the performance is considered numerically stable and matching the analytical expectation.

Calculate the slope using the standard simple linear regression formula:
`slope = (n * sum(x*y) - sum(x) * sum(y)) / (n * sum(x^2) - (sum(x))^2)`

Write your final results to `/home/user/report.txt` in exactly the following format:
```
SLOPE: <slope_value_rounded_to_2_decimal_places>
STATUS: <STABLE_CUBIC if slope is between 2.90 and 3.10, otherwise UNSTABLE>
```

Constraints:
- You must use standard shell utilities (e.g., `awk`, `grep`, `sed`, `bc`). Do not use Python or other scripting languages.
- Round the slope to exactly 2 decimal places in your final output (e.g., `3.01`).
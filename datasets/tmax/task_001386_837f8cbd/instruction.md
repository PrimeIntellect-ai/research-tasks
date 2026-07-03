You are a performance engineer tasked with profiling two new mathematical solver algorithms. You need to create a reproducible computational pipeline to test them, extract statistical metrics, and determine the performance regression/improvement.

The solvers are located at:
- `/home/user/solvers/solver_alpha`
- `/home/user/solvers/solver_beta`

Both solvers take a single integer argument representing the `run_id` (to ensure reproducibility) and print their execution time in milliseconds to standard output.

Your task:
1. Write a shell loop/pipeline to execute both `solver_alpha` and `solver_beta` exactly 100 times each. Pass the integers `1` to `100` (inclusive) as the `run_id` argument to the respective solver.
2. Capture the standard output of these runs.
3. Using standard Linux command-line tools (like `awk`, `sort`, `bc`, etc.), calculate the following for each solver:
   - **Mean** execution time.
   - **95th Percentile (P95)** execution time. (Calculate this by sorting the 100 outputs numerically and selecting the 95th value in the sorted list).
4. Determine which solver is faster on average (has the lower mean execution time).
5. Create a final report at `/home/user/perf_report.txt` with exactly the following format (replace the bracketed placeholders with your calculated values formatted to exactly 2 decimal places):

```
Alpha Mean: [value]
Alpha P95: [value]
Beta Mean: [value]
Beta P95: [value]
Faster Solver: [Alpha or Beta]
```

Constraints:
- You must accomplish this using standard terminal tools. 
- Ensure all values are rounded to exactly 2 decimal places in your final report.
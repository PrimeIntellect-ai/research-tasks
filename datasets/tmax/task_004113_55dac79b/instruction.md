You are a data scientist tasked with performing curve fitting using only basic shell tools. You do not have access to Python, R, or any advanced scientific environments. 

You have a dataset located at `/home/user/data.csv` containing two comma-separated columns: `x` and `y`.
Your goal is to fit a simple linear regression model ($y = mx + b$) to this data using a brute-force grid search optimization approach.

Write a Bash script (you may use `awk`, `bc`, and standard coreutils) that does the following:
1. Searches the parameter space for the slope `m` in the range `[0.0, 5.0]` with a step size of `0.1`.
2. Searches the parameter space for the intercept `b` in the range `[0.0, 5.0]` with a step size of `0.1`.
3. For each combination of `(m, b)`, calculates the Sum of Squared Errors (SSE) across all points in `/home/user/data.csv`.
4. Identifies the `m` and `b` that yield the minimum SSE.
5. Writes the optimal parameters and their corresponding SSE to a file named `/home/user/optimal_params.txt` in exactly this format (rounded/formatted to 2 decimal places for all values):
   `m=2.00, b=1.10, SSE=0.09`

Requirements:
- Do not use Python, Perl, or any non-POSIX/standard tools. Use Bash, `awk`, `bc`, `sed`, etc.
- Run your script to generate the final `/home/user/optimal_params.txt` file before finishing.
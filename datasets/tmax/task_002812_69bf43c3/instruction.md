You are an AI assistant helping a data scientist debug a distributed simulation. 

Our simulation recently underwent an update to its reduction algorithm, which changed the floating-point addition order. As a result, the output arrays across different runs are no longer perfectly bitwise identical, and we need to figure out which of the new candidate reduction methods produces data statistically closest to the original reference run.

You need to write a Bash pipeline/script that manages a scientific environment, performs linear regression to compare the datasets, and identifies the best match.

Here are your instructions:
1. Scientific Environment Management: 
   Create a Python virtual environment at `/home/user/sim_env`. Activate it and install `numpy`.

2. The Data:
   - Reference data: `/home/user/data/reference.txt` (a single column of floating point numbers).
   - Candidate runs: A directory `/home/user/data/candidates/` containing several `.txt` files (e.g., `run_alpha.txt`, `run_beta.txt`, etc.). Each has the same number of lines as the reference file.

3. The Analysis Script:
   Create a Bash script at `/home/user/evaluate_runs.sh`. When executed, this script must:
   - Use the Python virtual environment you created.
   - Iterate over all `.txt` files in `/home/user/data/candidates/`.
   - For each candidate file, treat the values in `/home/user/data/reference.txt` as the independent variable ($X$) and the candidate values as the dependent variable ($Y$).
   - Compute the linear regression coefficients: slope ($m$) and intercept ($c$).
   - Calculate a "deviation score" using the formula: $Score = (m - 1.0)^2 + (c - 0.0)^2$. (A perfect match would have $m=1, c=0$, and thus a score of 0).
   - Output the results for each file into `/home/user/regression_results.csv` with the exact format: `filename,slope,intercept,score` (where filename is just the basename, e.g., `run_alpha.txt`). Format the floats to 6 decimal places.
   - Identify the candidate file with the lowest deviation score and write ONLY its basename to a file at `/home/user/best_run.txt`.

Ensure your bash script is executable (`chmod +x`). You may write an inline Python script inside your Bash script to handle the `numpy` computations. Run your script to generate `/home/user/regression_results.csv` and `/home/user/best_run.txt`.
You are a Machine Learning Engineer preparing a dataset for a model that predicts user conversions. You have two raw data feeds that need to be deterministically joined, and you need to calculate the 95% confidence interval of the mean of a specific feature to establish baseline expectations.

Your task is to write a reproducible Bash pipeline script located at `/home/user/prepare_pipeline.sh`.

The script must perform the following actions:
1. Ensure numerical libraries are configured for single-threaded reproducible operations by exporting the environment variables `OPENBLAS_NUM_THREADS=1` and `PYTHONHASHSEED=0` at the very beginning of the script.
2. Read two comma-separated files (which do not have headers): 
   - `/home/user/user_metadata.csv` (Columns: `user_id`, `age`, `country`)
   - `/home/user/user_activity.csv` (Columns: `user_id`, `clicks`, `conversions`)
3. Sort and join these two files on the `user_id` column (the first column in both files) using standard Bash utilities (like `sort` and `join`).
4. Save the joined output to `/home/user/joined.csv`. The joined file should be comma-separated and contain 5 columns: `user_id`, `age`, `country`, `clicks`, `conversions`.
5. Calculate the sample mean and the 95% confidence interval for the mean of the `clicks` column (the 4th column in the joined data). 
   - Use the formula: `Mean ± 1.96 * (Sample_Standard_Deviation / sqrt(N))`
   - Use $N-1$ for the sample standard deviation calculation.
   - You may use a short embedded Python or awk script inside your bash pipeline to do this math.
6. Write the lower bound and upper bound of the confidence interval to `/home/user/ci_results.txt` in the format `lower_bound,upper_bound` (rounded to 2 decimal places).

Make sure the script `/home/user/prepare_pipeline.sh` has executable permissions, but do not execute it indefinitely—the automated test will run `/home/user/prepare_pipeline.sh` and then verify `/home/user/joined.csv` and `/home/user/ci_results.txt`.
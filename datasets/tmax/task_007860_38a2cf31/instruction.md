You are a data analyst troubleshooting a data pipeline. You have a raw dataset of sensor measurements at `/home/user/measurements.csv` with two columns: `id` and `value`. Some sensors malfunctioned, producing missing values (`NaN`, empty fields) and extreme outliers. 

Your task is to build a robust Bash-driven pipeline that cleans the data and computes a bootstrap confidence interval for the mean.

Write a Bash script at `/home/user/analyze.sh` that does the following:
1. **Missing Value & Outlier Handling**: Uses standard command-line tools (e.g., `awk`, `grep`, `sed`) to read `/home/user/measurements.csv`, skip the header, and extract only the `value` column. It must filter out any rows where the value is non-numeric, empty, or `NaN`. It must also filter out outliers, defined as values strictly greater than `1000` or strictly less than `-1000`. Save these cleaned, valid numbers to `/home/user/clean_values.txt` (one number per line).
2. **Sampling & Bootstrap Methods**: The Bash script should generate a Python script `/home/user/bootstrap.py` (using a heredoc or echo) and then execute it. The Python script must:
   - Read the numbers from `/home/user/clean_values.txt`.
   - Set the random seed via `import numpy as np; np.random.seed(42)`.
   - Perform a bootstrap by drawing 1000 random samples *with replacement*. Each sample must have the same size as the cleaned dataset.
   - Calculate the mean of each of the 1000 samples.
3. **Numerical Accuracy Testing**: The Python script should calculate the 2.5th and 97.5th percentiles of the 1000 bootstrap means using `np.percentile()`.
4. **Output formatting**: The Python script must print the confidence interval rounded to exactly two decimal places in the format `CI: [lower, upper]`. The bash script should capture this stdout and write it to `/home/user/final_ci.txt`.

Ensure your Bash script has execution permissions and runs correctly when executed as `bash /home/user/analyze.sh`.
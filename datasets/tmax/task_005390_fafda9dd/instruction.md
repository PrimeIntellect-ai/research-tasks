You are an assistant helping a data researcher organize and analyze their datasets using standard Linux CLI tools. 

I have a dataset located at `/home/user/dataset.csv`. The file is comma-separated and contains two columns with a header: `X,Y`.

I need you to write a Bash script at `/home/user/analyze.sh` that acts as a reproducible data pipeline. The script must be written using standard shell tools (like `gawk`, `sort`, `tail`, `head`, etc.) and MUST NOT use Python, R, or any other higher-level scripting languages.

The script must perform the following pipeline when run as `bash /home/user/analyze.sh`:

1. **Feature Engineering**: For each data row, compute a new feature $Z = X \times Y$.
2. **Bootstrap Resampling**: Generate 1,000 bootstrap samples (with replacement) of the $Z$ values. The size of each bootstrap sample must be equal to the number of data rows $N$ in the dataset.
3. **Statistic Calculation**: Calculate the mean of $Z$ for each of the 1,000 bootstrap samples.
4. **Hypothesis Testing / Confidence Intervals**: Determine the 95% confidence interval of the mean of $Z$ using the percentile method. Sort the 1,000 bootstrap means in ascending order. The lower bound is the 25th value (the 2.5th percentile) and the upper bound is the 975th value (the 97.5th percentile).
5. **Output**: Print the result exactly in this format to stdout: `CI: [lower_bound, upper_bound]` (round bounds to 4 decimal places).

**Reproducibility Constraint:**
To ensure pipeline reproducibility, you must perform the random sampling inside `gawk`. In your `gawk` script's `BEGIN` block, you MUST call `srand(123)` exactly once. To sample random indices with replacement, use the formula `idx = int(rand() * N) + 1` where `N` is the number of data rows. 

Make sure the script is executable. You can test your script on the provided `/home/user/dataset.csv`.
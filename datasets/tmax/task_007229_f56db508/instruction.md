I'm a researcher organizing experimental datasets, and I recently discovered a critical data leakage bug in my data processing pipeline. My previous aggregation script accidentally read the entire dataset when calculating prior probabilities, leaking information from the test set into the training set.

I have a dataset located at `/home/user/trials.csv` with the columns `id,group,success` (where success is either `0` or `1`). The file contains a header row followed by exactly 100 rows of experimental data.

Please write a bash script at `/home/user/analyze.sh` to properly perform the tabular data transformation and Bayesian updating without data leaks. The script must do the following:
1. Strictly separate the first 80 data rows (lines 2-81 of the file) to serve as the training set. 
2. Completely ignore the remaining 20 rows (the test set) to guarantee pipeline reproducibility and prevent data leaks.
3. For each `group` in the training set, calculate the Bayesian posterior mean of the success probability assuming a Beta(1, 1) prior (which equates to Laplace smoothing). 
   * The formula for the posterior mean is: `(number of successes in group + 1) / (total trials in group + 2)`.
4. Output the results to a tab-separated file at `/home/user/priors.tsv`.
5. The output file must not contain a header, should be sorted alphabetically by the `group` name, and formatted as `group \t posterior_mean`. 
6. The `posterior_mean` must be rounded to exactly 4 decimal places.

Your script must use standard bash tools (like `awk`, `sed`, `grep`, `sort`, `bc`, etc.) rather than Python or R, to minimize dependencies in our lightweight container environment. Ensure the script is executable or runnable via `bash /home/user/analyze.sh`.
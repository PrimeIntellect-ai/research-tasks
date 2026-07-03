You are an ML Engineer preparing a data pipeline to analyze customer transaction data. You have been provided with a dataset at `/home/user/transactions.csv`.

Your goal is to build a reproducible data pipeline consisting of a Bash validation script, a Python bootstrapping and plotting script, and a master Bash script to tie them together.

Step 1: Data Schema Enforcement
Write a Bash script at `/home/user/validate.sh` that takes a single file path as an argument. The script must verify:
1. The first line is exactly `transaction_id,amount,category`.
2. Every line in the file (including the header) has exactly 3 comma-separated fields.
If both conditions are met, the script should exit with status `0`. Otherwise, it should exit with status `1`.

Step 2: Bootstrapping and Plotting
Write a Python script at `/home/user/bootstrap.py` that does the following:
1. Reads `/home/user/transactions.csv`.
2. Sets `numpy.random.seed(42)` for reproducibility.
3. Generates 1000 bootstrap samples of the `amount` column. Each sample must be generated using `numpy.random.choice` with replacement, and the sample size must equal the total number of data rows in the CSV.
4. Calculates the mean of each bootstrap sample.
5. Calculates the 2.5th and 97.5th percentiles of these 1000 means and saves them to `/home/user/ci.txt` in the exact format `lower_bound,upper_bound` (rounded to 2 decimal places, e.g., `100.50,110.25`).
6. Generates a histogram of the 1000 means and saves it to `/home/user/plot.png`. **Crucially**, ensure this plotting works in a headless Linux environment by explicitly configuring the `matplotlib` backend (e.g., using `Agg`) before importing `pyplot`, otherwise it will fail or produce blank plots.

Step 3: Reproducible Pipeline
Write a master Bash script at `/home/user/pipeline.sh` that:
1. Calls `./validate.sh /home/user/transactions.csv`.
2. If the validation succeeds, executes `python3 bootstrap.py`.
3. If the validation fails, prints "Validation failed" and exits with status `1`.

Make sure all Bash scripts are executable. Do not run the pipeline yourself; just create the scripts.
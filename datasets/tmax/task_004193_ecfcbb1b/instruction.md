You are a Machine Learning Engineer responsible for preparing a large sensor dataset for a new predictive maintenance model. The data pipeline must be implemented completely using Bash and standard Linux command-line tools (e.g., `awk`, `grep`, `sed`, `split`, `shuf`).

Your pipeline must accomplish the following phases:

**Phase 1: Data Schema Enforcement**
Raw data is located in `/home/user/raw_data/` as multiple CSV files (without headers). 
Write a Bash script at `/home/user/scripts/validate.sh` that reads all `.csv` files in the raw data directory and filters out invalid rows based on the following schema:
- Column 1 (`id`): Must be a positive integer.
- Column 2 (`timestamp`): Must match the strict ISO-8601 format `YYYY-MM-DDTHH:MM:SSZ`.
- Column 3 (`sensor_val`): Must be a valid floating-point number (e.g., `12.34`, `-0.5`, `0.0`).
- Column 4 (`label`): Must be exactly `0` or `1`.
Save all valid rows combined into a single file at `/home/user/clean_data/combined.csv`.

**Phase 2: Large-Scale Storage Partitioning**
Partition `combined.csv` into two separate compressed files based on the `label` (Column 4).
- Rows with label `0` must be gzipped and saved to `/home/user/processed_data/label_0/data.csv.gz`.
- Rows with label `1` must be gzipped and saved to `/home/user/processed_data/label_1/data.csv.gz`.

**Phase 3: Statistical Summary (Hypothesis Testing Prep)**
Using standard command-line tools, compute the mean `sensor_val` for rows where label is `0` and the mean `sensor_val` for rows where label is `1`. 
Calculate the absolute difference between these two means.
Save the absolute difference (rounded to 4 decimal places) to `/home/user/metrics/mean_diff.txt`.

**Phase 4: Cross-Validation Splits**
Prepare the clean data for 5-fold cross-validation. 
Write a script at `/home/user/scripts/kfold.sh` that takes `/home/user/clean_data/combined.csv`, randomly shuffles the rows (use `shuf` with the random seed `--random-source=<(getconf CLK_TCK)` or any deterministic/non-deterministic seed, as long as it shuffles), and splits the data into 5 roughly equal files.
Save the files in `/home/user/cv_folds/` named `fold_1.csv`, `fold_2.csv`, `fold_3.csv`, `fold_4.csv`, and `fold_5.csv`.

**Constraints:**
- Ensure you create any directories that do not exist.
- Do not use Python, R, or Perl for the data processing tasks. You must use Bash, `awk`, `sed`, `grep`, etc.
- Execute your scripts so the final state contains all the requested output files.
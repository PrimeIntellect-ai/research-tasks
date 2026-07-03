Hello, I am a researcher organizing some experimental datasets, and I need your help fixing a data processing pipeline written in Bash. 

I have a raw dataset located at `/home/user/data/raw.csv`. It contains 100 rows of numeric data without a header. The three columns are `X1`, `X2`, and `y`.

I wrote a Bash script at `/home/user/scripts/prepare_data.sh` to split the data into training (first 80 rows) and testing (last 20 rows) sets, and to standardize (Z-score scale) the features `X1` and `X2`. However, I realized my script has a classic **data leak**: it calculates the mean and standard deviation over the *entire* dataset before splitting it! This means information from the test set is leaking into the training set.

Here is what you need to do:

1. **Fix the Data Leak**: 
   Modify `/home/user/scripts/prepare_data.sh` so that it first splits `/home/user/data/raw.csv` into `train_raw.csv` (first 80 lines) and `test_raw.csv` (last 20 lines). 
   Then, calculate the mean and standard deviation (population std dev) for `X1` and `X2` using **ONLY** `train_raw.csv`.
   Finally, use these training statistics to standardize both `train_raw.csv` and `test_raw.csv`, outputting the results to `/home/user/data/train_scaled.csv` and `/home/user/data/test_scaled.csv`. The `y` column (column 3) should remain unchanged. Use `awk` within your bash script for the floating-point math and CSV parsing.

2. **Implement Bootstrap Sampling**:
   Create a new Bash script at `/home/user/scripts/bootstrap.sh`. This script must read `/home/user/data/train_scaled.csv` and generate 5 bootstrapped datasets (sampling with replacement) named `boot_1.csv`, `boot_2.csv`, `boot_3.csv`, `boot_4.csv`, and `boot_5.csv` in the `/home/user/data/` directory. Each bootstrap sample must contain exactly 80 rows (the same size as the training set). Use Bash's `$RANDOM` for generating random indices.

**Expected Final State**:
- `/home/user/scripts/prepare_data.sh` runs successfully and correctly produces `/home/user/data/train_scaled.csv` and `/home/user/data/test_scaled.csv`.
- `/home/user/scripts/bootstrap.sh` runs successfully and produces the 5 bootstrapped files.
- The features in `test_scaled.csv` are scaled using the mean and standard deviation of `train_raw.csv`.

You can start by creating the raw dataset and the buggy script to simulate my environment, but your final goal is to produce the correct scripts and outputs. Assume I have already created `/home/user/data` and `/home/user/scripts` directories.
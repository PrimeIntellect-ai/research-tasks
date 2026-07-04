You are an assistant helping a data science researcher build a robust, pure-Bash data processing pipeline. The researcher wants to organize a large dataset, split it into training and testing sets, perform bootstrap sampling, and calculate covariance—all while strictly avoiding data leakage between the train and test sets.

Because of deployment constraints, this entire pipeline must be written using only standard Linux shell tools (Bash, awk, sed, coreutils, etc.) without relying on Python, R, or other external numerical libraries.

Write a Bash script named `/home/user/pipeline.sh` that takes two arguments:
1. The path to the input CSV dataset.
2. A path to a random source file (to ensure deterministic behavior for `shuf`).

The dataset is a CSV file with a header and three columns: `ID, Feature_X, Feature_Y`.

Your script `/home/user/pipeline.sh` must perform the following steps exactly in order:

1. **Storage & Splitting**: 
   - Extract the header and keep it aside.
   - Count the total data rows (excluding the header). Let this be `N`.
   - Split the data sequentially: the first 70% of rows (integer division: `train_n = N * 70 / 100`) form the initial training set, and the remaining rows form the test set.

2. **Bootstrap Sampling**:
   - Create a bootstrap sample of the training set. Specifically, use the `shuf` command with the provided random source file (`--random-source=$2`) to sample `train_n` rows **with replacement** from the initial training set. 
   - Ensure the `shuf` command is formatted as: `shuf --random-source="$2" -r -n "$train_n" ...`

3. **Preventing Data Leakage (Centering)**:
   - Calculate the mean of `Feature_X` and `Feature_Y` using **ONLY** the bootstrapped training set.
   - Subtract these training means from `Feature_X` and `Feature_Y` in **both** the bootstrapped training set and the test set. (This centers the data based purely on the training distribution, avoiding leakage).

4. **Covariance Analysis**:
   - Calculate the sample covariance between the centered `Feature_X` and `Feature_Y` of the **test set**.
   - Formula for sample covariance: `Sum(X_centered * Y_centered) / (test_n - 1)`.

5. **Output**:
   - The script should print a single floating-point number to standard output: the calculated sample covariance of the test set, formatted to exactly 4 decimal places (e.g., `12.3456`).

Ensure the script is executable (`chmod +x /home/user/pipeline.sh`).

For your own testing, you can create a dummy CSV file and a random source file (e.g., `dd if=/dev/urandom of=rand_source bs=1024 count=1`). The automated verification will run your script against a hidden dataset.
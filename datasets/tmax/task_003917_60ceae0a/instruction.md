You are an analyst auditing a data processing pipeline. A previous analyst made a "data leakage" mistake by normalizing a machine learning test dataset using its own mean and standard deviation, rather than the statistics from the training set. 

Your task is to fix this pipeline using ONLY Bash shell built-ins and standard POSIX utilities (like `awk`, `sed`, `grep`, `join`, `sort`, etc.). Do not use Python, R, or any other higher-level languages to process the data.

You have three files in `/home/user/`:
1. `/home/user/train.csv` - Contains training data. Columns: `id,feature_A,feature_B`
2. `/home/user/test.csv` - Contains test data. Columns: `id,feature_A,feature_B`
3. `/home/user/labels.csv` - Contains ground truth labels for the test data. Columns: `id,label`

Perform the following steps:
1. Parse `/home/user/train.csv` to calculate the mean ($\mu$) and **sample** standard deviation ($s$) of `feature_A`. (Ignore the header row).
2. Normalize `feature_A` in `/home/user/test.csv` using the training statistics: $Z = \frac{x - \mu}{s}$.
3. Join the normalized test data with `/home/user/labels.csv` on the `id` column.
4. Calculate the Mean Squared Error (MSE) between the normalized `feature_A` ($Z$) and the `label` for the test set. MSE = $\frac{1}{N} \sum_{i=1}^{N} (Z_i - label_i)^2$.
5. Save the final MSE, rounded to exactly 4 decimal places, into `/home/user/mse_result.txt`.

Constraints:
- Assume the first row of every CSV is a header.
- The `id` column is alphanumeric.
- Use the **sample** standard deviation formula (divide by $N-1$).
- Do not write a Python or Perl script. You must use standard shell tools (e.g., `awk` is highly recommended for the math).
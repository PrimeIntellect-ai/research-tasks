You are a data scientist tasked with cleaning a dataset, but you need to avoid "data leakage" where information from the test set influences the training set processing.

A raw dataset is located at `/home/user/data.csv`. It contains the following columns: `id`, `feature1`, `age`, `income`, `target`. 
The first row is the header. The next 800 rows are the training set, and any remaining rows are the test set.

Write a Bash script at `/home/user/clean.sh` that takes the path to the CSV file as its first argument and prints the processed dataset to standard output. Your script must perform the following steps:
1. **Missing Value Handling**: Compute the mean `age` from the training set ONLY. Impute any missing `age` values in the entire dataset (both train and test) with the integer floor of this training mean.
2. **Outlier Handling**: Compute the mean `income` from the training set ONLY. Cap any `income` values in the entire dataset at `2 * train_mean_income` (use the integer floor of this cap). If a row's `income` exceeds this cap, replace it with the cap.
3. **Data Schema Enforcement**: The output must only contain the columns `id`, `target`, `age`, `income` (in that exact order). 
4. The output must be valid CSV format with a header row reflecting the new column order.

Make sure your script is executable (`chmod +x /home/user/clean.sh`). You may use common Linux utilities (like `awk`, `sed`, `grep`) or inline Python within your Bash script to accomplish this.
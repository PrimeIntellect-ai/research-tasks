You are a Data Scientist reviewing a custom C-based data preprocessing pipeline. We've discovered a data leakage issue in the missing value imputation step.

Here is the situation:
We have a dataset at `/home/user/data.csv` containing 1000 rows of numerical data. The first column is `id`, and the second column is `feature_val`. Missing values in `feature_val` are encoded as `-999.0`.
The first 800 rows are the training set, and the remaining 200 rows are the test set.

Currently, the C program at `/home/user/pipeline.c` computes the mean of `feature_val` across the *entire* dataset (ignoring `-999.0`), and then replaces all missing values with this global mean. This is a classic data leak!

Your tasks:
1. Modify `/home/user/pipeline.c` so that the mean of `feature_val` is computed **strictly using the first 800 rows** (the training set). 
2. Use this training mean to impute missing values (`-999.0`) in the entire dataset (both train and test).
3. Have the C program output the final 200 rows (the imputed test set) to `/home/user/test_imputed.csv`. Format: `id,feature_val` (two decimal places for feature_val).
4. We have a proprietary stripped binary located at `/app/outlier_scorer`. It takes a CSV file path as an argument and prints an outlier score (between 0.0 and 1.0) for each row in the CSV file, line by line.
5. Run `/app/outlier_scorer /home/user/test_imputed.csv`. Remove any rows from `test_imputed.csv` where the corresponding outlier score is strictly greater than `0.80`. Save the filtered data to `/home/user/final_test.csv`.
6. Start an HTTP server on `127.0.0.1:8080` that serves the directory containing `final_test.csv` (so that a GET request to `http://127.0.0.1:8080/final_test.csv` downloads the file). The server must remain running in the background.

Ensure your C code compiles without warnings and handles the data correctly. Keep the server running so our automated verifier can download and check `final_test.csv`.
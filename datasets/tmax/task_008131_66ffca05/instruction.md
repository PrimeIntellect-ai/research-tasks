You are helping a researcher organize their dataset and fix a data leakage issue in their preprocessing pipeline. 

The researcher has a dataset located at `/home/user/data.csv` with two columns: `id,value`. The file contains a header row, followed by exactly 100 data rows. Some of the `value` entries are missing (empty strings, represented as `id,`).

Originally, the researcher calculated the mean, min, and max for the entire dataset to impute missing values and perform min-max scaling, and *then* split the data into training and testing sets. This caused a data leak, as information from the test set influenced the training set's preprocessing.

Your task is to write a Bash script at `/home/user/process.sh` that performs the preprocessing correctly using standard Linux command-line tools (e.g., `awk`, `sed`, `head`, `tail`).

The script must execute the following logic:
1. Perform a train/test split: The first 80 data rows (after the header) are the training set. The remaining 20 data rows are the test set.
2. Calculate the mean of the `value` column using *only* the valid (non-empty) entries in the training set.
3. Calculate the minimum and maximum of the `value` column using *only* the valid entries in the training set.
4. Impute missing values: For any empty `value` in either the training or test set, replace it with the training mean.
5. Min-max scale the values: For every row in both sets, scale the `value` using the training min and max: `scaled_value = (value - train_min) / (train_max - train_min)`.
6. Format the scaled values to exactly 4 decimal places (e.g., `0.1230`).
7. Output the processed data (including the `id,value` header) to `/home/user/train_processed.csv` and `/home/user/test_processed.csv` respectively.

Ensure your script has executable permissions (`chmod +x /home/user/process.sh`) and run it so the output files are generated.
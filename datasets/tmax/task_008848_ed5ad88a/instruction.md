You are a data analyst investigating a potential data leakage issue in a machine learning pipeline. You suspect that some records in the test set were inadvertently scaled using parameters specific to individual train records, resulting in identical `feature_hash` values but slightly different `confidence` scores due to numerical instability.

You have been provided with two CSV files:
1. `/home/user/train_data.csv`
2. `/home/user/test_data.csv`

Both files have the following header-less format:
`id,feature_hash,prediction,confidence`

Your task is to identify the data leak and compute the numerical discrepancy. 
Using standard Linux command-line tools (like `awk`, `join`, `sort`, etc.), perform the following:
1. Find all instances where a `feature_hash` in `test_data.csv` exactly matches a `feature_hash` in `train_data.csv`.
2. For these leaked records, calculate the absolute difference between the `confidence` value in the train set and the `confidence` value in the test set. (Assume `feature_hash` is unique within each file).
3. Output the results to a file named `/home/user/leak_report.csv`.

The output file `/home/user/leak_report.csv` must:
- Contain exactly two comma-separated columns: `feature_hash` and the absolute `confidence` difference.
- Format the confidence difference to exactly 3 decimal places (e.g., `0.050`).
- Be sorted in descending numerical order by the confidence difference. If there are ties, sort them alphabetically by `feature_hash` in ascending order.
- Contain no headers.
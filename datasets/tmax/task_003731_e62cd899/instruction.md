You are an MLOps engineer tracking experiment artifacts. You have a directory of model output files located at `/home/user/experiments`. Each file is a CSV containing predictions from a different model run. 

The CSV files share the following schema:
`id,model_name,prediction,confidence`

Your task is to filter, validate, and compute a bootstrap statistic on these artifacts. Specifically, you must:

1. **Size Filtering**: Identify all CSV files in `/home/user/experiments` that are at least 50 kilobytes in size. Ignore smaller files.
2. **Output Validation**: Check the `confidence` column of the files that passed the size filter. A file is considered "valid" only if ALL of its `confidence` values are between 0.0 and 1.0 (inclusive). If a file contains any confidence value less than 0.0 or greater than 1.0, exclude the entire file.
3. **Data Aggregation**: Concatenate the records from all CSV files that passed both the size and validation checks.
4. **Bootstrap Sampling**: Using Python, read this combined dataset and extract the `prediction` column. Perform a bootstrap sample by drawing exactly 1000 records from the combined `prediction` data. You **must** sample with replacement and use a random seed of 42 (e.g., using `pandas.Series.sample(n=1000, replace=True, random_state=42)`).
5. **Reporting**: Calculate the mean of these 1000 bootstrap-sampled predictions. Round the mean to exactly 4 decimal places.
6. Save this single rounded number to a file named `/home/user/bootstrap_mean.txt`.

Ensure your logic strictly follows the exact filtering order and random seed specification.
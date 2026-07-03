You are tasked with cleaning a dataset of model predictions and generating a reproducible bootstrap sample for further analysis. 

A large dataset of raw model outputs is located at `/home/user/inference_data.csv`. This CSV file contains the following columns: `id`, `feature_1`, `prediction_score`, and `label`.

Due to upstream pipeline errors, the dataset contains several corrupted rows. You must write a Python script (or use command-line tools) to process the file according to the following rules:

1. **Clean the Data**: 
   - Filter out any rows where the `prediction_score` cannot be parsed as a float, or falls outside the valid probability range of `[0.0, 1.0]` (inclusive).
   - Filter out any rows where the `label` is not exactly `"A"` or `"B"`.
   
2. **Bootstrap Sampling**:
   - From the strictly cleaned dataset, draw a bootstrap sample (sampling with replacement) of exactly `50` rows.
   - You MUST use `pandas` to perform the sampling, specifically using `df.sample(n=50, replace=True, random_state=42)` to ensure reproducibility.
   
3. **Output**:
   - Save the final bootstrapped sample as a CSV file to `/home/user/bootstrapped_clean.csv`.
   - The output must include the CSV header and maintain the original column order. Do not include the pandas dataframe index (`index=False`).

Complete this task by executing your solution in the terminal.
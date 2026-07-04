You are tasked with processing two datasets for a mathematical analysis pipeline. You must perform a multi-source data join, handle the missing values, and apply dimensionality reduction. 

You have been provided with two CSV files in `/home/user/data/`:
1. `/home/user/data/dataset_A.csv`: Contains columns `id`, `f1`, `f2`, `f3`.
2. `/home/user/data/dataset_B.csv`: Contains columns `id`, `f4`, `f5`.

Write a Python script at `/home/user/process.py` and execute it to perform the following steps:
1. Perform a full **outer join** of `dataset_A` and `dataset_B` using the `id` column.
2. Sort the resulting combined dataset by `id` in ascending order.
3. Fill any missing values (NaNs) in the feature columns (`f1`, `f2`, `f3`, `f4`, `f5`) with the integer `0`.
4. Extract the feature matrix (columns `f1` through `f5` in that exact order).
5. Apply Principal Component Analysis (PCA) to reduce these 5 features down to 2 dimensions (`pc1`, `pc2`). 
   - Use `sklearn.decomposition.PCA`.
   - Set `n_components=2`.
   - Set `svd_solver='full'` and `random_state=42` to ensure reproducibility.
6. Save the results to `/home/user/pca_result.csv`. The output CSV must have exactly three columns: `id`, `pc1`, `pc2` (in that order).
   - **Crucial Formatting Requirement:** The `id` column in your output CSV MUST be strictly formatted as integers (e.g., `1`, `2`, `100`), not floats (e.g., `1.0` is incorrect). Pay close attention to how your data joining might silently alter data types!
   - Include the header row in the output.
   - Values in `pc1` and `pc2` should be standard floats.

Run your script so that `/home/user/pca_result.csv` is produced.
You are a data analyst tasked with writing a Bash-based ETL pipeline. 

We have a dataset located at `/home/user/raw_data.csv` containing four columns: `record_id`, `dataset_split`, `val_x`, and `val_y`.
Your objective is to clean this data, calculate normalization statistics, and apply a z-score normalization without causing data leakage between the train and test splits.

Write a Bash script (using standard tools like `awk`, `sed`, `grep`, `bc`, etc.) at `/home/user/process_data.sh` that performs the following steps:

1. **Data Cleaning & Schema Enforcement**:
   - Filter out any rows that have missing (empty) values for `val_x` or `val_y`.
   - Filter out any rows where `val_y` is exactly the string `"NA"` or `"NULL"`.
   - Filter out any rows where `val_x` is strictly less than 0 (outlier handling).
   - *Note: Ensure the CSV header is handled correctly and not treated as a data row during math operations.*

2. **Calculate Statistics (Prevent Data Leakage)**:
   - Calculate the population mean ($\mu$) and population standard deviation ($\sigma$) for `val_x` and `val_y`.
   - **CRITICAL**: You must calculate these statistics using ONLY the rows where `dataset_split` is `"train"` (after applying the cleaning rules in Step 1). Calculating statistics over the entire dataset causes train-test leakage. 

3. **Apply Transformation**:
   - Apply z-score normalization to `val_x` and `val_y` for ALL valid rows (both `"train"` and `"test"`), using the $\mu$ and $\sigma$ calculated from the train set in Step 2.
   - Formula: $z = \frac{x - \mu}{\sigma}$

4. **Formatting and Output**:
   - Save the final dataset to `/home/user/processed_data.csv`.
   - The output file must have the header: `record_id,dataset_split,norm_x,norm_y`.
   - The data rows must be sorted numerically by `record_id`.
   - Format `norm_x` and `norm_y` to exactly 4 decimal places (e.g., `0.0000`, `-1.2247`).

Execute your script so that `/home/user/processed_data.csv` is generated successfully.
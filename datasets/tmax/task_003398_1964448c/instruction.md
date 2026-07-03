You are a Machine Learning Engineer tasked with building a reliable ETL and modeling pipeline in Rust. A previous implementation suffered from "data leakage" because it computed scaling statistics and imputed missing values using the *entire* dataset before splitting into train and test sets.

Your job is to write a Rust program that processes a raw dataset, avoids data leakage, and trains a simple 1-dimensional Ordinary Least Squares (OLS) linear regression model.

**Dataset:** 
You will find a CSV file at `/home/user/raw_sensor_data.csv` with columns: `id`, `sensor_id`, `reading_value`, `target_value`.

**Pipeline Requirements:**
You must implement the following steps exactly in this order:

1. **Schema & Outlier Filtering (Data Cleaning):**
   - Read the CSV.
   - Drop any rows where `sensor_id` is less than 1 or greater than 100.
   - Drop any rows where `reading_value` is explicitly provided but is greater than 1000.0 (outliers).
   - Maintain the original sequential order of the remaining valid rows.

2. **Train/Test Split:**
   - Split the remaining valid rows into a Train set and a Test set sequentially.
   - The Train set must contain exactly the first 80% of the rows. The Test set contains the remaining 20%. (Use integer division: `train_count = total_valid_rows * 8 / 10`).

3. **Leakage-Free Imputation & Scaling:**
   - Compute the `mean` and *sample* standard deviation (`std`) of the `reading_value` using **only** the valid, non-missing values in the **Train set**.
   - Impute any missing (empty) `reading_value`s in *both* the Train and Test sets using the computed Train `mean`.
   - Standardize the `reading_value`s in *both* sets using the Train `mean` and Train `std`. Formula: `scaled_value = (original_value - train_mean) / train_std`.

4. **Model Training:**
   - Train a 1D Ordinary Least Squares linear regression model on the **Train set** to predict `target_value` using the `scaled_value` as the input feature.
   - Calculate the weight ($w$) and bias ($b$) using standard OLS formulas.

**Output Generation:**
Your Rust program should write a JSON file to `/home/user/pipeline_results.json` containing the following keys (all values as floats rounded to 4 decimal places):
- `"train_mean"`: The mean used for imputation and scaling.
- `"train_std"`: The sample standard deviation used for scaling.
- `"weight"`: The computed OLS weight ($w$).
- `"bias"`: The computed OLS bias ($b$).
- `"test_first_scaled_reading"`: The `scaled_value` of the very first row in the Test set.

You may use any Rust crates you need (e.g., `csv`, `serde`, `serde_json`). Build and run your Rust program to generate the required output file.
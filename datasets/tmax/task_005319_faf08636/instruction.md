You are an ETL data engineer debugging a data pipeline issue using standard Linux terminal tools. You recently discovered that a downstream model failure was caused by an upstream bug that silently converted expected integer predictions into floats (e.g., adding `.0`) or introduced missing values (NaNs/blanks).

You need to create a Bash script that joins two data sources, validates the output, and performs simple dimensionality reduction by removing redundant features.

Write a Bash script at `/home/user/etl_check.sh` that does the following:

1. **Multi-source Data Joining**: 
   Join the two CSV files located at `/home/user/sourceA.csv` and `/home/user/sourceB.csv` on their `id` columns. Assume both files have headers.
   - `sourceA.csv` format: `id,f1,f2`
   - `sourceB.csv` format: `id,f3,pred`

2. **Model Output Validation**:
   Inspect the joined data. The `pred` column must contain only valid integers (e.g., `100`, `-5`). 
   - Identify any `id` where `pred` is empty, missing, or contains a decimal point (e.g., `200.0`). 
   - Extract the `id`s of these invalid rows and save them, one per line, to `/home/user/invalid_ids.txt`. Keep this list sorted numerically.

3. **Correlation and Dimensionality Reduction**:
   Compare the `f1` column (from source A) and the `f3` column (from source B) for all rows (including invalid ones). 
   - If `f1` and `f3` are perfectly correlated (i.e., they have the exact same values for every joined row), apply dimensionality reduction by dropping the `f3` column from the final dataset. 
   - If they differ in even one row, keep both columns. (For this dataset, assume they *will* be perfectly correlated, but your script should technically drop `f3` from the output layout).

4. **Output Generation**:
   Save the final cleaned, joined dataset to `/home/user/clean_joined.csv`. 
   - The file must be comma-separated.
   - It must include the header. Assuming `f3` is dropped, the header should be `id,f1,f2,pred`.
   - It must **exclude** any rows that failed the model output validation in step 2.
   - Sort the output numerically by `id`.

Constraints:
- You must write the solution entirely in a Bash script (`/home/user/etl_check.sh`).
- You may use standard shell utilities (`awk`, `join`, `sort`, `cut`, `sed`, `grep`, etc.), but you **cannot** use Python, Perl, Ruby, or R.
- Ensure the script has executable permissions and works standalone.
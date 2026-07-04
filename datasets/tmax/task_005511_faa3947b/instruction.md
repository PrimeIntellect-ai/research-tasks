You are a data engineer building a lightweight ETL pipeline using Bash. 

You have been given three CSV files in `/home/user/data/`:
1. `train.csv` - Contains `id` and `reading`. Some `reading` values are missing (empty strings).
2. `test.csv` - Contains `id` and `reading`. Some `reading` values are missing.
3. `meta.csv` - Contains `id` and `factor` for all ids in both train and test sets.

You need to write a Bash script at `/home/user/process_etl.sh` that processes these files to output `train_final.csv` and `test_final.csv` into the same directory. 

To prevent **data leakage** between the train and test sets, all imputation statistics and scaling parameters must be calculated **strictly from the training dataset**.

Your script must perform the following steps:
1. **Join Data**: Join `train.csv` and `test.csv` with `meta.csv` based on `id`.
2. **Missing Value Imputation**: Calculate the arithmetic mean of the `reading` column in `train.csv` (ignoring missing values). Use this *train mean* to fill any missing `reading` values in both `train.csv` and `test.csv`.
3. **Adjustment**: Create a new adjusted value for each row: `adjusted_reading = imputed_reading * factor`.
4. **Min-Max Scaling**: Calculate the minimum and maximum of the `adjusted_reading` values exclusively from the **training set**. Scale the `adjusted_reading` values in both train and test sets using the formula: `scaled_value = (adjusted_reading - train_min) / (train_max - train_min)`.
5. **Output**: Write the results to `train_final.csv` and `test_final.csv`. 
    - The output files must have the header `id,scaled_adjusted_reading`.
    - Sort the output by `id` numerically in ascending order.
    - Output the `scaled_adjusted_reading` formatted to exactly 4 decimal places (e.g., `0.2000`).

Ensure your script is executable and can run directly in the shell without any arguments. Do not use Python; rely on standard Unix tools like `awk`, `join`, `sort`, etc.
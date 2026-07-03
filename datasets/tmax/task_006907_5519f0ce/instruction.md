You are a data analyst tasked with building a reproducible ETL pipeline to process regional sales data. 

You have been provided with three CSV files in `/home/user/data/`:
1. `us_sales.csv`
2. `eu_sales.csv`
3. `uk_sales.csv`

The data comes from different regional systems, so the `Revenue` column is formatted inconsistently:
- US data uses `$` and `.` for decimals (e.g., `$1500.50`).
- EU data uses `,` for decimals and has no currency symbol (e.g., `1500,50`).
- UK data uses `£` and `.` for decimals (e.g., `£1200.75`).

Your task is to write a reproducible Python script at `/home/user/pipeline.py` that performs the following ETL steps:
1. **Extract**: Read all three CSV files.
2. **Transform**:
   - Normalize the `Revenue` column into a standard numerical float format (handling the different currency symbols and decimal separators).
   - Filter the dataset to include ONLY rows where the normalized `Revenue` is strictly greater than `1000.00`.
   - Aggregate the data to calculate the total valid revenue per `Region`.
3. **Load**: 
   - Ensure the directory `/home/user/output/` exists.
   - Save the aggregated results to `/home/user/output/summary.csv`.
   - The output CSV must have exactly two columns: `Region` and `Total_Revenue`.
   - The rows must be sorted alphabetically by `Region`.
   - `Total_Revenue` must be formatted to exactly two decimal places (e.g., `3500.50`).

Run your pipeline script so the output file is generated.
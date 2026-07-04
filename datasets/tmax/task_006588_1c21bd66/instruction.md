You are an AI assistant helping a data researcher organize and validate their recent model output datasets. 

The researcher has placed several CSV files in `/home/user/raw_data/`. Each file contains the predictions of a different model run. 
The CSV files have the following header: `id,condition,score,status`.

Your task is to write and execute a Bash workflow (using standard tools like `awk`, `sed`, `grep`, `sort`, etc.) to accomplish the following:

1. **Environment Setup:** Create a new directory structure for the clean data. Create a directory named `/home/user/analysis/` containing two subdirectories: `valid/` and `invalid/`.
2. **Model Output Validation:** Process all `.csv` files in `/home/user/raw_data/`. A row (excluding the header) is considered **valid** if:
   - The `status` is exactly `SUCCESS`.
   - The `score` is a numeric value between `0.0` and `1.0` (inclusive).
3. **Data Transformation:** 
   - Extract all valid rows from all CSV files and append them (without the header) into a single file at `/home/user/analysis/valid/combined.csv`.
   - Any rows that fail the validation criteria (excluding headers) should be appended to `/home/user/analysis/invalid/rejected.csv`.
4. **Aggregation:** Using only the valid rows, calculate the average `score` for each unique `condition`. 
5. **Reporting:** Save the aggregated results to `/home/user/analysis/summary.tsv`. This file must be tab-separated, contain no header, and have two columns: the `condition` and the `average_score` (formatted to exactly two decimal places, e.g., `0.75`). The rows in this file must be sorted alphabetically by `condition`.

Use pure Bash and standard POSIX utilities (like `awk`) to complete this task.
You are a log analyst investigating anomalous server behavior. You have received a raw, corrupted log file of system metrics and a screenshot of a legacy dashboard containing the baseline reference values. 

Your goal is to build an ETL pipeline in Python to extract, clean, impute, and store these metrics, and calculate their deviations from the baseline.

**Inputs provided:**
1. `/app/legacy_dashboard.png`: An image of an old dashboard. You must extract the text to find the "BASELINE_LATENCY" value (a floating-point number).
2. `/home/user/raw_metrics.csv`: A messy log file with columns: `timestamp`, `cpu_usage`, `memory_usage`, `latency`.

**Task Requirements:**
1. **Environment & OCR**: Use standard Python tools (e.g., `pytesseract`, `Pillow`) to extract the `BASELINE_LATENCY` value from `/app/legacy_dashboard.png`.
2. **Data Cleaning & Normalization**:
   - Read `/home/user/raw_metrics.csv`.
   - The `timestamp` column contains a mix of ISO-8601 strings and UNIX epoch integers. Standardize them all to Python datetime objects in UTC.
   - Any rows with negative values in `cpu_usage` or `memory_usage` are corrupt. Drop these rows.
   - Implement pipeline logging: write a log entry for every dropped row to `/home/user/pipeline.log` in the format: `[WARNING] Dropped corrupt row at <original_timestamp>`.
3. **Resampling & Imputation**:
   - The metrics are irregularly spaced. Set the timestamp as the index and resample the entire dataset to a strictly **1-minute frequency**, starting from the earliest valid timestamp to the latest.
   - For any missing periods (gaps) created by resampling or dropped rows, use **linear interpolation** to fill the missing values for `cpu_usage`, `memory_usage`, and `latency`.
4. **Data Transformation**:
   - Create a new column called `normalized_latency` by subtracting the `BASELINE_LATENCY` (extracted from the image) from the interpolated `latency` values.
5. **Database Import**:
   - Bulk insert the cleaned, resampled, and transformed dataset into a SQLite database at `/home/user/system_metrics.db` in a table named `cleaned_metrics`.
6. **Final Export**:
   - Export just the `timestamp` (as ISO-8601 string) and `normalized_latency` columns of the final resampled dataframe to a CSV file at `/home/user/final_output.csv`.

Ensure your final CSV contains no missing values and exactly follows the 1-minute frequency. Your performance will be evaluated by comparing your `final_output.csv` to a hidden, perfectly reconstructed dataset using Mean Squared Error (MSE).
You are an automation specialist tasked with building a robust data processing pipeline. We have a system that exports server metrics to a CSV file, but the export tool is buggy. Occasionally, it includes multiline logs in the "notes" field (embedded newlines inside double quotes). Our downstream analytics engine crashes if it encounters these embedded newlines. 

Your objective is to write a script in the language of your choice that reads the raw data, applies strict filtering and transformations, and produces a normalized, reshaped output.

**Input Data:**
File: `/home/user/data/raw_metrics.csv`
Columns: `timestamp,host,cpu_load,memory_usage,disk_io,notes`

**Requirements:**
1. **Filtering (Regex & Dropping):** You must identify and silently drop any row where *any* field contains an embedded newline character (`\n` or `\r\n`). Do not attempt to fix or merge these rows; drop the entire row completely.
2. **Normalization:** The `timestamp` column comes in two mixed formats: `YYYY/MM/DD` and `MM-DD-YYYY`. You must standardize all valid timestamps to the ISO 8601 format: `YYYY-MM-DD`.
3. **Reshaping (Wide to Long):** Convert the three metric columns (`cpu_load`, `memory_usage`, `disk_io`) from a wide format into a long format. The resulting columns should be `date`, `host`, `metric_name`, and `metric_value`. Note that `date` is the normalized `timestamp` column.
4. **Outputs:**
   - Save the reshaped, cleaned CSV to `/home/user/output/clean_long.csv`. The header must be exactly `date,host,metric_name,metric_value`. The rows must be sorted chronologically by `date`, then by `host`, and then alphabetically by `metric_name`.
   - Use a text template to generate a summary report at `/home/user/output/summary.txt`. The file must exactly match this format:
     ```
     Pipeline Execution Summary
     --------------------------
     Dropped invalid rows: <X>
     Total valid metric records generated: <Y>
     ```
     *(Where `<X>` is the number of raw rows dropped due to embedded newlines, and `<Y>` is the total number of data rows in `clean_long.csv` excluding the header).*

**Constraints:**
- The agent will run this script to completion and create the required files.
- The directory `/home/user/output` must be created if it does not exist.
- Ensure all permissions are standard user level.
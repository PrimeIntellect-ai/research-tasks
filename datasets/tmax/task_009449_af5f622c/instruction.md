You are a Data Scientist working entirely in a Linux terminal. You have received a raw dataset of server telemetry, but it is messy and needs to be cleaned, validated, and augmented before it can be ingested by a downstream machine learning model.

The raw dataset is located at `/home/user/server_metrics.csv`.

Your task is to write a Bash-based pipeline (using tools like `awk`, `sed`, `grep`, etc.) to process the file and generate a cleaned dataset at `/home/user/cleaned_metrics.csv`.

Perform the following operations:
1. **Schema Enforcement**: Ensure every data row has exactly 5 columns separated by commas. Furthermore, ensure that columns 2, 3, 4, and 5 are strictly numeric (they may contain decimal points or negative signs, but no other characters). Drop any rows that do not meet these criteria.
2. **Feature Engineering**: Append a 6th column named `mem_cpu_ratio`. This should be calculated as `mem_usage` (Column 3) divided by `cpu_usage` (Column 2). If `cpu_usage` is exactly `0` or `0.0`, the ratio should be set to `0.00` to avoid division by zero. Ensure this new column is formatted to exactly 2 decimal places (e.g., `22.51`, `0.00`).
3. **Feature Selection (Filtering)**: The downstream model only cares about servers running hot. Retain only the rows where `temp` (Column 5) is strictly greater than `40.0`.
4. **Header handling**: Your output file `/home/user/cleaned_metrics.csv` must include the header row, updated to reflect the new 6th column: `timestamp,cpu_usage,mem_usage,disk_io,temp,mem_cpu_ratio`.
5. **Numerical Accuracy Test**: Calculate the arithmetic mean of the newly engineered `mem_cpu_ratio` column across all valid, filtered data rows. Save this single average value (formatted to exactly 2 decimal places) into a file named `/home/user/feature_mean.txt`.

Ensure your solution handles the data robustly using standard shell utilities without relying on external scripting languages like Python or R.
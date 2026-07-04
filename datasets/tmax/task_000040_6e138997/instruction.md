You are a data engineer tasked with building a lightweight ETL and testing pipeline for a legacy Linux environment where Python, R, and other high-level languages are strictly forbidden. You must use only standard shell tools (Bash, `awk`, `sed`, `grep`, `bc`, etc.).

The input data is located at `/home/user/server_metrics.csv`. It contains server telemetry data with a header row.
Columns: `ID,CPU,RAM,DiskIO,Status`

You must implement a multi-stage Bash-only pipeline that accomplishes the following:

**Phase 1: Data Schema Enforcement**
1. Read `/home/user/server_metrics.csv` (skip the header for processing, but include a valid header in the output).
2. Filter out rows that violate the schema. A valid row must have exactly 5 comma-separated columns. `ID`, `CPU`, `RAM`, and `DiskIO` must be either numeric values (integers or decimals) or the exact character `?` (representing missing data). `Status` must be either `OK` or `FAIL`.
3. Save the valid rows (with the original header) to `/home/user/schema_valid.csv`.

**Phase 2: Missing Value and Outlier Handling**
1. Read `/home/user/schema_valid.csv`.
2. Missing Value Imputation: Replace any `?` in the `CPU` column with the fixed value `50.0`, and any `?` in the `RAM` column with the fixed value `50.0`.
3. Outlier Handling: Cap any `RAM` value strictly greater than `100.0` to exactly `100.0`.
4. Save the cleaned rows (with the header) to `/home/user/cleaned.csv`.

**Phase 3: Feature Engineering**
1. Read `/home/user/cleaned.csv`.
2. Add a new 6th column named `Load_Factor`.
3. The value of `Load_Factor` is calculated as `(CPU * RAM) / 100`. Format this value to exactly 2 decimal places.
4. Save the new dataset (with the updated header `ID,CPU,RAM,DiskIO,Status,Load_Factor`) to `/home/user/engineered.csv`.

**Phase 4: Model Training and Evaluation (Threshold Search)**
We want to predict if a server will `FAIL` based on the `Load_Factor`. Our "model" is a simple threshold: If `Load_Factor >= T`, predict `FAIL`, otherwise predict `OK`.
1. Write a bash script (or `awk` one-liner) to evaluate all integer thresholds `T` from `1` to `100`.
2. For each threshold, calculate the Accuracy (number of correct predictions divided by total valid rows, excluding the header).
3. Find the integer threshold `T` that yields the highest accuracy. If there is a tie, pick the lowest `T`.
4. Output the result to a file named `/home/user/best_model.txt` with exactly the following format (replace `X` with the integer threshold and `Y.YY` with the accuracy rounded to 2 decimal places):
`Best Threshold: X, Accuracy: Y.YY`

Ensure all file paths and names match exactly. Do not use Python, Perl, or any external binaries not found in a standard GNU coreutils/util-linux installation.
We are migrating away from a proprietary data cleaning pipeline. The legacy system is a compiled binary located at `/app/legacy_pipeline`. It ingests two CSV datasets (Users and Transactions), joins them, handles missing values, removes outliers, engineers aggregate features, and outputs a cleaned CSV to standard output.

Your task is to write a Python script at `/home/user/clean_data.py` that perfectly replicates the behavior of `/app/legacy_pipeline`. We will run an automated fuzzing suite that feeds random datasets into both the legacy binary and your Python script. Your script's output must be **bit-exact equivalent** to the binary's output for all inputs.

**Data Schemas:**
Users CSV:
- `user_id`: 64-bit integer (can be up to 19 digits).
- `age`: integer (contains missing values).
- `risk_score`: float.

Transactions CSV:
- `txn_id`: 64-bit integer.
- `user_id`: 64-bit integer.
- `amount`: 64-bit integer (contains missing values).
- `status`: string.

**Observed Pipeline Logic (You must verify this via black-box testing against the binary):**
1. Multi-source join: Left join Users and Transactions.
2. Missing value handling: Missing `age` must be imputed with `99`. Missing `amount` must be imputed with `0`.
3. Outlier handling: Any transaction where `amount` > `1000000` or `amount` < `-1000000` is dropped entirely *before* aggregation.
4. Feature engineering: Group by user and compute `total_amount` (sum of amounts) and `txn_count` (number of valid transactions). Users with no valid transactions should have a `total_amount` of `0` and `txn_count` of `0`.
5. Numerical accuracy warning: `user_id` and `amount` use the full 64-bit integer space. Naive pandas operations (like introducing NaNs during a left join) silently cast integers to `float64`, which destroys precision for large integers (e.g., `9223372036854775807`). Your output must retain exact string representations of these integers without `.0` decimals or scientific notation.

**Execution Signature:**
Your script must accept exactly two positional arguments:
`python3 /home/user/clean_data.py <path_to_users.csv> <path_to_txns.csv>`
It must print the resulting CSV to `stdout` (including header: `user_id,age,risk_score,total_amount,txn_count`).

**Experiment Tracking:**
Additionally, your script must optionally accept a `--track <filepath>` flag. If provided, write a JSON file to `<filepath>` containing exactly:
`{"outliers_dropped": <int>, "ages_imputed": <int>}`

Develop your script, test it against `/app/legacy_pipeline` using your own mock data, and ensure pandas precision pitfalls are avoided.
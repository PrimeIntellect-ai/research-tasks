You are a data scientist debugging a Bash-based data processing pipeline. A previous pipeline attempted to join datasets using loose joins, which silently introduced empty fields (similar to NaNs in Pandas) and broke downstream model validation. You need to write a robust Bash script to merge the data, enforce a strict schema, validate model predictions, and compute benchmark metrics.

You are given three tab-separated value (TSV) files in `/home/user/data/`. They do NOT contain headers.
1. `users.tsv`: Columns are `user_id`, `age`, `country`.
2. `predictions.tsv`: Columns are `user_id`, `model_id`, `score`.
3. `latency.tsv`: Columns are `user_id`, `latency_ms`.

Write a script at `/home/user/clean_and_benchmark.sh` that performs the following tasks:
1. **Multi-source joining**: Join the three files on `user_id`. Only keep users that are present in all three files (inner join).
2. **Schema Enforcement & Model Validation**: Filter the joined data to keep ONLY rows that strictly match all the following criteria:
   - `age` must be a positive integer (greater than 0).
   - `score` must be a valid floating-point number between `0.0` and `1.0` (inclusive).
   - `latency_ms` must be a positive integer (greater than 0).
3. **Data Export**: Save the perfectly clean, joined, and filtered data to `/home/user/valid_joined.tsv`. The columns must be in this exact order: `user_id`, `age`, `country`, `model_id`, `score`, `latency_ms` (tab-separated).
4. **Inference Performance Benchmarking**: Using the clean data, calculate the average `latency_ms` for each `model_id`.
5. **Report Generation**: Save the benchmark results to `/home/user/benchmark_report.tsv`. It must be tab-separated, with `model_id` and the average latency formatted to exactly two decimal places (e.g., `120.00`). Sort this report alphabetically by `model_id`.

Constraints:
- Use standard bash tools (e.g., `awk`, `join`, `sort`). You may not use Python, Perl, or other higher-level scripting languages.
- Be careful with missing fields or silent data type conversions.

Once you have written the script, execute it to generate `/home/user/valid_joined.tsv` and `/home/user/benchmark_report.tsv`.
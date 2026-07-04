You are a log analyst investigating user activity patterns for a web application. 

You have been given a raw log file located at `/home/user/raw_logs.jsonl`. Each line is intended to be a JSON object containing event data, but the logging system introduced several formatting and data quality issues that currently break downstream parsers like `jq`.

Your task is to write a Bash script at `/home/user/process_logs.sh` that reads `/home/user/raw_logs.jsonl` and produces a clean, validated JSON Lines file at `/home/user/clean_logs.jsonl`.

The script must perform the following pipeline operations:

1. **Unicode/Escape Sequence Processing:** The logging system incorrectly wrote ASCII/UTF-8 hex escapes as `\xNN` (e.g., `\x21`, `\x2E`) inside JSON strings. Standard JSON only supports `\u00NN` for these. You must find all instances of `\xNN` (where N is a hex digit) and convert them to the standard JSON unicode escape format `\u00NN`.
2. **Interpolation/Imputation:** Some log entries failed to capture the `user_id`, resulting in `"user_id": null`. You must impute these missing values by replacing `null` with the string `"UNKNOWN"`.
3. **Data Masking/Anonymization:** To comply with privacy policies, you must mask the `email` field. Replace the "local part" of the email address (everything before the `@` symbol) with exactly three asterisks `***`. For example, `"alice.smith@example.com"` must become `"***@example.com"`.
4. **Validation Checkpoint:** Ensure that the final `/home/user/clean_logs.jsonl` contains only valid JSON lines. 

Write the Bash script `/home/user/process_logs.sh`, make it executable, and run it to generate the final file.

**Output Requirements:**
- The final file `/home/user/clean_logs.jsonl` must have exactly the same number of lines as the input file.
- Every line must be valid JSON parseable by `jq`.
- Keys order in the output JSON lines does not matter as long as the structure is valid and values are correct.
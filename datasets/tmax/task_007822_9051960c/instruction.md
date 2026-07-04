You are a log analyst investigating patterns in a global application's diagnostic logs. You have received a raw, messy log file located at `/home/user/app_logs.jsonl`. The logs contain multi-language user feedback and system metrics, but they are plagued by duplicates, missing values, and inconsistent Unicode encoding.

Write a Python script (and run it) to process this file and generate a clean version at `/home/user/processed_logs.jsonl`.

Your processing pipeline must perform the following steps:
1. **Unicode Normalization:** Read each JSON object and normalize the `feedback_text` field using Unicode **NFKC** normalization. After normalization, strip any leading and trailing whitespace.
2. **Hash-based Deduplication:** Calculate the MD5 hash of the *normalized and stripped* `feedback_text` encoded as UTF-8. Keep only the *first* log entry for each unique hash (earliest by `timestamp`). Discard any subsequent entries that have the exact same normalized feedback text hash.
3. **Sorting:** Sort the deduplicated logs chronologically by `timestamp` in ascending order.
4. **Interpolation & Imputation:** The `cpu_temperature` field has missing values (represented as `null`). Use linear interpolation to fill in these missing values based on the sorted sequence. If there are `null` values at the very beginning or end of the dataset, use backward fill and forward fill respectively to handle them. Round the final temperature values to 1 decimal place.
5. **Text Processing:** Add a new field `text_length` to each log, which is the integer count of Unicode characters in the normalized and stripped `feedback_text`.

**Input Schema (`app_logs.jsonl`):**
- `timestamp` (integer): Unix epoch time.
- `log_id` (string): Unique identifier for the log.
- `feedback_text` (string): The raw feedback text in various languages (contains emojis, unnormalized unicode, etc.).
- `cpu_temperature` (float or null): System temperature metric.

**Output Schema (`processed_logs.jsonl`):**
Must be a valid JSONL file where each line is a JSON object containing:
- `timestamp` (integer)
- `log_id` (string)
- `feedback_text` (string) - *Normalized and stripped*
- `cpu_temperature` (float) - *Interpolated/Imputed and rounded to 1 decimal place*
- `text_length` (integer) - *Character count of the normalized/stripped text*

Ensure your output is strictly sorted by `timestamp` ascending.
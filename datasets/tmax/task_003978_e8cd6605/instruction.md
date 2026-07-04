You are an engineer managing configuration states for a global fleet of servers. An unreliable ETL job recently failed and retried multiple times, resulting in a large output file containing duplicate configuration records.

Your task is to write a Python script to process the raw configuration file, filter out invalid data, remove duplicates using hash-based deduplication, and output a clean file. 

**Input File:**
`/home/user/raw_configs.jsonl`
Each line is a JSON object with the following schema:
- `server_id` (string)
- `timestamp` (integer - UNIX epoch)
- `retry_id` (integer)
- `config_data` (object): Contains `app_name` (string), `settings` (object), and `description` (string, which includes multi-language Unicode characters like Chinese, Arabic, and Russian).

**Requirements for your Python script:**

1. **Validation Checkpoint:** Discard any record where the `config_data` object is missing the `app_name` key entirely or if `app_name` is null.
2. **Hash-Based Deduplication:** The ETL job produced identical configurations under different `timestamp`s and `retry_id`s. Two records are considered identical duplicates if they have the exact same `server_id` and the exact same `config_data`. 
   - To deduplicate, compute a SHA-256 hash of the `server_id` and `config_data`. To ensure consistency, serialize `config_data` to a JSON string with keys sorted, no extra spaces (i.e., `separators=(',', ':')`), and ensure Unicode characters are NOT escaped (`ensure_ascii=False`). Concatenate `server_id` and this JSON string, then hash the utf-8 encoded result.
   - When duplicates are found, **keep the record with the earliest (minimum) `timestamp`** and discard the others.
3. **Parallel Processing:** You must use Python's `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` to perform the validation and hash computation across multiple CPU cores. 
4. **Output:** 
   - Write the cleaned, deduplicated records to `/home/user/clean_configs.jsonl`.
   - The output must be valid JSON Lines.
   - The output must preserve Unicode characters natively (do not escape them to `\uXXXX`).
   - The final output file must be sorted alphabetically by `server_id`. If there are multiple unique configurations for the same `server_id` (e.g., they changed over time), sort them by `timestamp` ascending.

Write and execute your Python script to generate `/home/user/clean_configs.jsonl`.
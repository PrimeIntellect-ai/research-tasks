You are a data engineer building an ETL pipeline to process and join chat logs and transaction logs. You have been given two datasets, but the ingestion system introduced some formatting issues.

Your task is to write a Rust program that cleans, joins, and aggregates these datasets.

**Input Files:**
1. `/home/user/chat_logs.jsonl`: Contains chat messages.
   Format: `{"session_id": "<string>", "timestamp": "<ISO8601 string>", "message": "<string>"}`
   *Issue:* The ingestion system double-escaped Unicode sequences in the `message` field. For example, the JSON string literal contains `"Hello \\u3053"`, which parses into a Rust String containing the literal characters `H`, `e`, `l`, `l`, `o`, ` `, `\`, `u`, `3`, `0`, `5`, `3`. 

2. `/home/user/tx_logs.jsonl`: Contains transactions.
   Format: `{"session_id": "<string>", "timestamp": <Unix epoch integer seconds>, "amount": <float>}`

**Your Rust Program Must:**
1. Be created in `/home/user/etl_processor` (you will need to initialize a cargo project here).
2. Read both JSONL files.
3. Clean the `message` field in the chat logs:
   - Identify literal `\uXXXX` sequences (where X is a hex digit) and decode them into their proper Unicode characters.
   - Normalize the resulting string using Unicode Normalization Form KC (NFKC).
4. Parse the timestamps to a common format (Unix epoch seconds).
5. For each chat message, calculate the rolling sum of transaction `amount`s from the same `session_id` that occurred strictly *after* the chat message's timestamp, but *within 60 seconds* (i.e., `chat_ts < tx_ts <= chat_ts + 60`). If there are no matching transactions, the sum is `0.0`.
6. Output the final aggregated data as a JSON-lines file to `/home/user/output.jsonl`.
   Format: `{"session_id": "<string>", "normalized_message": "<string>", "chat_ts": <Unix epoch integer seconds>, "tx_sum": <float>}`
7. The output file must be sorted by `chat_ts` in ascending order. If two chat logs have the exact same `chat_ts`, maintain their original relative order from `chat_logs.jsonl`.

Write the Rust code, build it, and run it to produce `/home/user/output.jsonl`. You may use standard crates like `serde`, `serde_json`, `chrono`, `regex`, and `unicode-normalization`.
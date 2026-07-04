You are acting as a data scientist cleaning incoming user log datasets. We need you to write a stream processing script that performs data masking, normalization, tokenization, joins, and basic anomaly filtering.

You have been provided with a local custom package at `/app/vendored/text_cleaner_lib`. Unfortunately, there is a deliberate bug in its source code that prevents it from working correctly.

Your goals:
1. Fix the bug in the `/app/vendored/text_cleaner_lib` package and install it locally so your script can use it.
2. Write a Python script at `/home/user/process_stream.py` that reads a stream of JSON Lines (JSONL) from standard input (`sys.stdin`) and writes the processed JSONL to standard output (`sys.stdout`).

Input JSONL format:
`{"user_id": <int>, "message": <str>, "timestamp": <str>}`

Processing requirements for each line:
1. **Join**: Look up the `user_id` in `/app/lookup.csv` (which has columns `user_id,region,risk_score`).
2. **Anomaly Detection**: If the `risk_score` from the lookup table is strictly greater than `90`, this is considered an anomaly. **Drop the record entirely** (do not output it). If the `user_id` is missing from the CSV, assume a `risk_score` of 0 and `region` of `"UNKNOWN"`.
3. **Data Masking & Tokenization**: Use the functions from the fixed `text_cleaner_lib` package on the `message` field:
   - First, redact any email addresses using `text_cleaner_lib.redact_emails(message)`.
   - Then, tokenize and normalize the redacted message using `text_cleaner_lib.tokenize_and_normalize(message)`.
4. **Output**: Print a JSONL object to standard output containing:
   `{"user_id": <int>, "region": <str>, "clean_tokens": [<str>, ...], "timestamp": <str>}`
   *Ensure the output keys are strictly as above and standard `json.dumps()` is used.*

Please ensure your script processes input efficiently and line-by-line. Your script's output behavior will be rigorously tested against an exact reference implementation using randomly generated input streams.
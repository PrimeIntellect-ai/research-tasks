You are tasked with building a robust Data Processing ETL pipeline for a configuration management tracker. 

Currently, our system relies on a Python Flask webhook receiver that dumps configuration changes into a wide-format CSV. However, this pipeline silently drops or corrupts rows containing embedded newlines (a common occurrence in valid JSON or shell script configuration values). 

You must implement a high-performance C-based sanitizer and reshaper that fixes this issue, and wire it up to our live service stack.

**System Architecture & Multi-Service Integration:**
In `/app/`, you will find a multi-service environment managed by a script `/app/start_services.sh`. It starts:
1. A Redis datastore (port 6379)
2. A Python Flask API (port 5000) that receives raw configuration webhooks.

The Flask API writes raw wide-format CSV lines to a named pipe `/tmp/config_stream.pipe`. 
You need to reconfigure the Flask application (source at `/app/api/app.py`) so it properly quotes CSV fields containing newlines, preventing the current truncation issue. Then, ensure your C program reads continuously from this pipe and writes valid configuration states to Redis.

**The C Sanitizer (`/home/user/csv_tracker.c`):**
Write a C program that reads the wide-format CSV from `stdin` and reshapes, filters, and computes metrics for each update.

*Input Format:*
The input CSV has no header. Each row contains 6 fields:
`id, timestamp, old_config_A, new_config_A, old_config_B, new_config_B`
(Fields are standard RFC 4180 CSV, separated by commas, and fields with embedded newlines or commas are enclosed in double quotes).

*Reshaping (Wide to Long):*
For each wide row, output two long-format records (one for config_A, one for config_B) with the following columns:
`id, timestamp, config_name, old_val, new_val, edit_distance`
(Where `config_name` is either the literal string `"config_A"` or `"config_B"`).

*Distance Computation:*
`edit_distance` must be the exact Levenshtein distance between the `old_val` and `new_val` strings.

*Sanitization Rules (Adversarial Filtering):*
You must silently DROP the reshaped record (do not output it) if EITHER of these conditions are met:
1. The `old_val` or `new_val` contains malicious shell characters. Specifically, reject the record if the values match the POSIX Extended Regular Expression: `[`$|<>]`
2. The Levenshtein distance between `old_val` and `new_val` is strictly greater than `50` (indicating a potential anomaly or denial-of-service payload).

*Output:*
Your compiled program must print the surviving, reshaped records to `stdout` in standard CSV format (fields containing commas/newlines must be double-quoted).

**Validation Corpora:**
We have provided two test corpora to evaluate your C filter's correctness against adversarial payloads and embedded newlines:
- `/app/corpora/clean/`: Contains CSV files with valid configurations (including legitimate embedded newlines). Your filter MUST preserve and reshape 100% of these records.
- `/app/corpora/evil/`: Contains CSV files with malicious payloads, regex anomalies, and extreme distance anomalies. Your filter MUST reject 100% of the evil records.

Write the code, compile it to `/home/user/csv_tracker`, update the API, and leave the system running.
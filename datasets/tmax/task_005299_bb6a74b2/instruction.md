You are a log analyst investigating patterns of malicious log injections and system anomalies. Your company uses a proprietary, legacy anomaly detector located at `/app/analyzer`. This stripped binary processes JSON log entries one by one to determine if they are anomalous (malicious/corrupted) or clean. It returns exit code 1 for anomalous/evil logs, and exit code 0 for clean logs.

However, `/app/analyzer` is painfully slow, occasionally crashes on malformed inputs instead of failing gracefully, and cannot be integrated into our new Python-based streaming pipeline. 

Your task is to write a Python replacement script at `/home/user/sanitizer.py` that exactly replicates the binary's filtering logic.

The logs are JSONL formatted with the following fields:
- `timestamp`: A string representing the event time, but originating from different systems (formats vary, e.g., ISO8601, Epoch, RFC2822).
- `message`: A free-text string that may contain multi-language text and Unicode characters.
- `metrics`: A list of floating-point numbers representing system readings. Some values are missing and represented as `null`.

You must reverse-engineer or black-box test the `/app/analyzer` binary to determine its precise rules for:
1. Timestamp alignment and validation.
2. Unicode and multi-language text processing (specifically how it handles normalization or malicious encoding).
3. Interpolation of missing (`null`) metric values.
4. Anomaly and changepoint detection on the imputed metrics.

Once you understand the rules, implement `/home/user/sanitizer.py`.
Your script must accept a single command-line argument (the path to a JSONL log file) and print ONLY the "clean" JSON logs to standard output (one valid JSON string per line), preserving the original JSON structure of the accepted lines. It should silently drop the anomalous/evil lines.

You can create dummy JSONL files to feed into `/app/analyzer` to figure out its behavior.

Requirements:
- Your script must be written in Python 3.
- Do not call the `/app/analyzer` binary from your Python script (the verification environment will test your script's standalone throughput). You must implement the logic natively in Python.
- Output lines must be valid JSON matching the exact original line of accepted logs.
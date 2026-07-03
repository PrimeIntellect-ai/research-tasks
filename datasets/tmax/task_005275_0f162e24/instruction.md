You are a log analyst investigating error patterns in a multilingual application's event stream. 

Your organization uses a proprietary Python package called `log_extractor` to decode incoming binary log payloads. We have provided the source code for this package in `/app/vendor/log_extractor-1.0`. However, the package is currently broken: it was written assuming all logs are in English, and it crashes with a decoding error when it encounters multilingual logs. 

Your tasks are as follows:

1. **Fix and Install the Package**: 
   Inspect the source code of the `log_extractor` package in `/app/vendor/log_extractor-1.0`. Find the bug preventing it from correctly decoding UTF-8 bytes, fix it, and install the package into your system Python environment.

2. **Develop the Analysis Pipeline**:
   Write a Python script at `/home/user/analyzer.py` that reads a single JSON object from **standard input** (STDIN). The input JSON will have the following format:
   `{"uid": <integer>, "raw_b64": "<base64_encoded_string>"}`

   Your script must:
   - Parse the JSON and decode the `raw_b64` field from base64 into raw bytes.
   - Use the fixed `log_extractor.parse_log(log_bytes)` function to convert the bytes into a Unicode string.
   - Calculate summary statistics: find the exact character count of the decoded string.
   - Perform anomaly detection: flag the log as an anomaly if the decoded string contains ANY of the following substrings (case-sensitive): `"🚨"`, `"CRÍTICO"`, `"严重"`, `"KRITISCH"`.
   - Output a single, strictly-formatted JSON object to **standard output** (STDOUT) representing the analysis result, matching exactly this format:
     `{"uid": <integer>, "message_length": <integer>, "is_anomaly": <boolean>}`

3. **Pipeline Logging**:
   For every log processed, append a single line to `/home/user/pipeline.log` in this exact format:
   `[INFO] Processed uid <uid>`

Ensure your script handles standard input correctly, processes the data cleanly without emitting any extra debug text to STDOUT, and produces the exact JSON structure requested. An automated verifier will test your script against thousands of random multilingual inputs to verify bit-exact behavioral equivalence with our oracle system.
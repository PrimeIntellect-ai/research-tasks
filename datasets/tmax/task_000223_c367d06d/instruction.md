You are a log analyst investigating strange patterns in a new system's logs. The logs are delivered as JSON lines, but the text parsing logic has been lost, save for a screenshot of the original specification.

You need to write a Python script located at `/home/user/process_log.py` that processes a single JSON log entry from standard input and prints the normalized token string to standard output.

Here are your instructions:
1. Read an image located at `/app/mapping.png`. This image contains the exact step-by-step normalization pipeline you must apply to the log messages. Use OCR (e.g., `tesseract`) to read it.
2. Your script `/home/user/process_log.py` must read a single line of JSON from `sys.stdin`.
3. The JSON will contain a key `"message"` with a string value. This string frequently contains double-escaped unicode sequences (e.g., `\\u0041` instead of the actual character 'A') that break standard parsers.
4. Extract the `"message"` string, apply the exact pipeline described in the image, and print the final resulting string to `sys.stdout` without any trailing newline (use `end=""` in print).
5. The script must be deterministic and perfectly match the expected output. It will be aggressively tested against random fuzzed inputs to ensure bit-exact equivalence with the reference implementation.

Do not print anything else to stdout other than the final normalized string.
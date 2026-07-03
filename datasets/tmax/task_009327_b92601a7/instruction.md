You are an operations engineer triaging an incident. Our data processing pipeline relies on a Python script, `/home/user/transformer.py`, to transform JSON lines from standard input into processed JSON lines on standard output. 

Recently, we noticed that we are intermittently dropping valid records. We suspect this happens when the stream contains corrupted JSON inputs (e.g., malformed syntax). Instead of just logging or yielding an error record, the transformer seems to be losing previously processed valid records when it attempts to recover from the corrupted input.

Your task:
1. Analyze `/home/user/transformer.py` to identify the bug in its error handling logic.
2. Fix the script so that when it encounters a `json.JSONDecodeError`, it appends `{"error": "corrupted"}` to the current batch, but **does not** discard any previously accumulated valid records in that batch.
3. Save your corrected script to `/home/user/fixed_transformer.py`.
4. To prove the fix works via diff analysis, create a test file at `/home/user/test_input.jsonl` with exactly three lines in this order:
   - Line 1: A valid JSON object `{"id": 1}`
   - Line 2: A corrupted, invalid JSON string (e.g., `{"id": 2, bad syntax}`)
   - Line 3: A valid JSON object `{"id": 3}`
5. Run your `fixed_transformer.py` using `test_input.jsonl` as standard input, and redirect the output to `/home/user/test_output.jsonl`.

Ensure all files are placed in `/home/user` and exactly match the requested filenames.
You are a log analyst investigating a pattern of strange multi-lingual log entries in our systems. Your sysadmin left you an automated voice alert containing a crucial "salt" string used for our log hashing system. 

First, listen to or transcribe the audio file located at `/app/voicemail.wav` to extract the secret salt (it will be a single lowercase English word). You can use any available tools (like `ffmpeg`, Python libraries, or `whisper` if installed) to figure out what the word is.

Second, you must create a Python script at `/home/user/log_filter.py` that acts as a stream processor. This script will be rigorously tested by an automated fuzzer that passes thousands of generated log lines into its standard input and expects bit-exact standard output.

The script must do the following for each line read from standard input:
1. Parse the line as a JSON object. If a line is not valid JSON, silently drop it and continue.
2. Expect the JSON to contain at least `user_id` (integer) and `message` (string). 
3. Perform Unicode normalization on the `message` field using the NFKC form.
4. Compute the SHA-256 hash of the normalized message concatenated with the secret salt (e.g., `hash(normalized_message + salt)`). Use UTF-8 encoding before hashing.
5. Deduplicate: Keep track of the hex digests of the hashes. If you have already seen this exact hash during the execution of the script, drop the log entry.
6. Mathematical Stratification: Look at the last 4 characters of the SHA-256 hex digest. Convert this 4-character hex string to a base-16 integer. If this integer is strictly divisible by 3 (i.e., `val % 3 == 0`), keep the log; otherwise, drop it.
7. For logs that pass all the above criteria, update the JSON object so its `message` field contains the NFKC-normalized string, and add a new field `"hash"` containing the full SHA-256 hex digest.
8. Print the updated JSON object to standard output on a single line (using `json.dumps` with no extra indentation), followed by a newline.

Your final program must be executable via `python3 /home/user/log_filter.py`. Ensure it processes stdin line-by-line efficiently.
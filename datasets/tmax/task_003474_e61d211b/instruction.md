You are a storage administrator managing disk space on a critical Linux server. An application has been generating massive log files because it occasionally embeds large hex-encoded binary core dumps directly inside the plain-text multi-line logs.

Your task is to write and execute a Python script (`/home/user/clean_logs.py`) that processes a specific log file located at `/home/user/storage/raw_app.log`.

The log file contains normal log entries, but occasionally contains a multi-line hex-encoded dump enclosed by specific markers:
`===BEGIN DUMP===`
and
`===END DUMP===`

Your script must:
1. Read `/home/user/storage/raw_app.log`.
2. Extract all the hex-encoded data found between `===BEGIN DUMP===` and `===END DUMP===`. Ignore whitespace and newlines within the hex data.
3. Decode this combined hex string into actual binary bytes.
4. Save the decoded binary data to a new file at `/home/user/storage/payload.bin`. (Assume there is only one dump in the file for this task).
5. Create a new log file at `/home/user/storage/cleaned_app.log` that is identical to the original log, EXCEPT that the `===BEGIN DUMP===`, the hex data, and the `===END DUMP===` lines are completely removed and replaced by a single line reading exactly: `[DUMP EXTRACTED TO PAYLOAD.BIN]`

Ensure your script processes the files efficiently. Once written, execute the script so that the output files are generated.
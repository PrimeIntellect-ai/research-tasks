You are a data scientist tasked with cleaning a messy dataset of user logs. The data is currently stored in a JSON-Lines file, but it suffers from inconsistent formatting, raw Unicode escape sequences, mixed timestamp formats, and exposed Personally Identifiable Information (PII).

Write a Bash script at `/home/user/clean.sh` that reads the file `/home/user/raw_data.jsonl` and produces a cleaned JSON-Lines file at `/home/user/clean_data.jsonl`.

Your script must perform the following operations on each JSON object:

1. **Key Normalization**: Convert all top-level JSON keys to strictly lowercase (e.g., `User_Name` becomes `user_name`, `TIMESTAMP` becomes `timestamp`).
2. **Unicode Normalization**: Ensure that any JSON-encoded Unicode escape sequences (e.g., `\u00e9`, `\u30c6`) in the string values are properly evaluated and output as literal UTF-8 characters.
3. **Data Masking (Anonymization)**: The `email` field contains full email addresses. Mask the local part (everything before the `@` symbol) completely by replacing it with exactly three asterisks `***`. For example, `alice.smith@example.com` must become `***@example.com`.
4. **Feature Extraction**: Extract the domain part of the original unmasked email address (everything after the `@`) and store it in a new top-level field called `email_domain`.
5. **Timestamp Alignment**: The `timestamp` field is wildly inconsistent. It contains either:
   - A string representing Epoch seconds (e.g., `"1672531200"`)
   - A string in the format `"YYYY-MM-DD HH:MM:SS"` (e.g., `"2023-01-02 15:30:00"`)
   Convert both formats to a strict ISO-8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`.

Requirements:
- Your script must be written in Bash and be executable (`chmod +x /home/user/clean.sh`).
- You may use standard command-line tools like `jq`, `awk`, `sed`, `date`, etc.
- The output file `/home/user/clean_data.jsonl` must contain valid JSON-Lines, with exactly one JSON object per line, in a compact format (no pretty-printing).
- You can assume `jq` is installed on the system.
You are an engineer managing a configuration tracking system. You have been given a raw log file at `/home/user/raw_logs.jsonl` that contains JSON Lines of configuration updates. 

Unfortunately, the logging system sometimes writes malformed unicode escape sequences (e.g., `\u00Z9`) that cause standard JSON parsers to crash. 

Your task is to create a complete data processing pipeline. Write a Bash script at `/home/user/run_pipeline.sh` that performs the following steps when executed:

1. **Pre-processing / Parsing**: Reads `/home/user/raw_logs.jsonl` and gracefully handles or strips malformed unicode escape sequences (specifically sequences starting with `\u` that are not followed by 4 valid hex digits) so that the lines can be successfully parsed as JSON.
2. **Extraction**: Extracts all `key=value` configuration changes from the unstructured `update_text` field in each JSON object. You can assume keys and values consist only of alphanumeric characters, underscores, or hyphens, and are separated by an equals sign (`=`).
3. **Anonymization**: Masks any extracted value where the key contains the substrings `password`, `token`, `key`, or `secret` (case-insensitive). Replace these sensitive values exactly with `***`.
4. **Loading**: Writes the processed records to a new JSON-lines file at `/home/user/clean_logs.jsonl`. Each line must be a valid JSON object with exactly two keys: `id` (the original integer ID) and `configs` (a dictionary of the extracted and potentially masked key-value pairs).

Example output format for a single line in `/home/user/clean_logs.jsonl`:
`{"id": 123, "configs": {"timeout": "30", "admin_password": "***"}}`

Requirements:
- Only output lines that were successfully parsed and processed.
- The script `/home/user/run_pipeline.sh` must be executable and orchestrate the entire workflow. You may write auxiliary scripts (e.g., in Python, Perl, or Ruby) if your bash script calls them.
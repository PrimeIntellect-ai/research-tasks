You are a web developer building a CI dashboard feature that tracks specific Rust compiler errors. Your team wants to analyze how often developers run into Rust ownership and borrow checker issues. 

Currently, the CI pipeline outputs `cargo check --message-format=json` logs into a legacy JSONL (JSON Lines) format. You need to write a Bash script that deserializes this log, filters for borrow checker errors, and migrates the data into a new simplified JSON schema for the web dashboard frontend.

Write a Bash script at `/home/user/process_logs.sh` that does the following:
1. Reads from the input file `/home/user/cargo_logs.jsonl`.
2. Deserializes the JSON objects.
3. Filters for messages where the `reason` is `"compiler-message"` and the `message.code.code` is `"E0382"` (a standard Rust borrow checker/ownership error).
4. Performs a schema migration by extracting specific fields and serializing them into a single, well-formed JSON array of objects.
5. Saves the output to `/home/user/dashboard_data.json`.

The new schema for each object in the JSON array must be exactly:
```json
{
  "error_code": "<the error code string, e.g., E0382>",
  "file": "<the file_name from the FIRST span in the message.spans array>",
  "line": <the line_start integer from the FIRST span in the message.spans array>
}
```

Constraints:
- The script must be written in Bash and must be executable. You may use standard CLI tools like `jq`.
- The final output in `/home/user/dashboard_data.json` must be a valid JSON array (`[...]`), not separate JSON lines.
- Ensure the script runs successfully and produces the output file before completing the task.
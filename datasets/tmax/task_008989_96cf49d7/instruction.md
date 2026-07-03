I need you to help me organize some raw application logs for a specific project. 

I have a compressed log file located at `/home/user/raw_data/system_logs.gz`. This file contains newline-separated JSON logs from multiple different projects. 

Please write and execute a Go script at `/home/user/parse_logs.go` that does the following:
1. Opens and streams the compressed file `/home/user/raw_data/system_logs.gz` directly using Go's `compress/gzip` and `bufio` packages. Do not extract the file to disk first.
2. Parses each line as JSON. The JSON structure is: `{"timestamp": "<string>", "project": "<string>", "level": "<string>", "message": "<string>"}`.
3. Filters for log entries where the `project` is exactly `"x-ray"` and the `level` is exactly `"FATAL"`.
4. Writes the raw JSON string of these matching lines (exactly as they appeared in the source, preserving the original formatting and trailing newline) to a destination file.
5. **CRITICAL:** The writing process must be atomic. You must write the output to a temporary file inside `/home/user/project_xray/` first, ensure all data is flushed to disk, and then atomically rename it to the final destination: `/home/user/project_xray/fatal.log`. 

The directory `/home/user/project_xray/` already exists. Write the Go script, compile or run it, and ensure `/home/user/project_xray/fatal.log` is created according to these rules.
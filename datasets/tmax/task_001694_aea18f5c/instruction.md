You are a log analyst investigating patterns in a web application's access logs. The logs are stored in a JSON-Lines (JSONL) format at `/home/user/access_logs.jsonl`. 

Due to a bug in a legacy upstream service, some log entries contain malformed unicode escape sequences (e.g., `\uXXXX` where the hex characters are invalid or cut off). Standard JSON parsers often break on these lines. Additionally, some log entries might be valid JSON but are missing the required `ip` field due to corrupted data ingestion.

Your task is to write a Python script that streams through this large log file, filters out the bad data using a quality gate, and computes summary statistics.

**Requirements:**
1. **Streaming processing**: Process the file `/home/user/access_logs.jsonl` line-by-line to avoid high memory consumption.
2. **Quality Gate / Validation**:
   - Attempt to parse each line as a JSON object.
   - A line is considered **invalid** if it throws a JSON decoding error (e.g., due to the malformed unicode escapes) OR if it successfully parses but is missing the `"ip"` key.
   - A line is considered **valid** if it successfully parses as JSON AND contains an `"ip"` key.
3. **Summary Statistics**:
   - Keep a count of the total number of **valid** lines.
   - Keep a count of the total number of **invalid** lines.
   - Determine the top 3 most frequent IP addresses among the valid lines (in descending order of frequency). If there is a tie, order the tied IPs alphabetically.
4. **Output**: Write your final aggregated statistics to a JSON file at `/home/user/summary.json` with the exact following schema:
```json
{
  "valid_lines": <int>,
  "invalid_lines": <int>,
  "top_ips": ["<ip1>", "<ip2>", "<ip3>"]
}
```

Ensure your script is robust and correctly handles the decoding errors without crashing. The output file `/home/user/summary.json` must be strictly formatted as requested so automated checks can verify your work.
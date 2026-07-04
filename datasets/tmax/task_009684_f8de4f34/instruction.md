You are a log analyst investigating a new pattern of errors on your company's servers.

A background service has dumped a batch of raw logs into `/home/user/raw_logs.txt`.
The log format is highly irregular. Each line consists of three pipe-separated (`|`) sections:
`TIMESTAMP | IP_ADDRESS | ERROR_COUNTS_JSON`

Example:
`2023-11-01T08:14:22Z | 192.168.1.100 | {"auth_fail": 2, "db_timeout": 0, "rate_limit": 1}`

Your task is to write a Go program (`/home/user/analyzer.go`) that performs the following data processing pipeline:
1. **Tokenization & Normalization**: Parse the pipe-delimited file. Clean any leading/trailing whitespace from the sections.
2. **Time-based Bucketing**: Truncate the timestamps to the nearest hour (e.g., `2023-11-01T08:14:22Z` becomes `2023-11-01T08:00:00Z`).
3. **Wide-long format reshaping & Aggregation**: The JSON object represents a "wide" format of error counts. Reshape this into a long format, aggregating (summing) the counts of each error type per hourly bucket across all log lines.
4. **Template-based text generation**: Use Go's `text/template` package to generate a Markdown report summarizing the findings. The output must be written to `/home/user/summary.md`.

The output markdown MUST exactly match the following format and be sorted chronologically by hour, and then alphabetically by error type:

```markdown
# Log Summary

## Hour: 2023-11-01T08:00:00Z
- auth_fail: 3
- db_timeout: 1
- rate_limit: 2

## Hour: 2023-11-01T09:00:00Z
...
```
*(Only include error types that have a count > 0 in that hour)*

Write the Go program, compile it, and run it to produce `/home/user/summary.md`.
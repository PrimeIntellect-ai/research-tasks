You are acting as a log analyst investigating a data pipeline issue. An ETL job that processes multi-lingual customer feedback failed and was retried multiple times, resulting in a massive amount of duplicate records in our logs.

We have a legacy normalization tool located at `/app/normalizer`. This tool reads a raw UTF-8 string from `stdin` and outputs a normalized string to `stdout`. It is heavily used to detect duplicate messages, but calling this binary as a subprocess for millions of log lines is far too slow. 

Your task is to write a highly efficient Go program at `/home/user/analyze.go` that:
1. Re-implements the exact text normalization logic used by the `/app/normalizer` binary. You will need to interact with the binary to reverse-engineer its behavior (it processes Unicode text, handles casing, and strips certain character classes).
2. Reads a JSONL log file (provided as the first command-line argument). Each line has the format: `{"id": "...", "lang": "...", "message": "..."}`
3. Computes summary statistics and stratified data using your re-implemented normalization function on the `message` field.
4. Outputs the results to `/home/user/summary.json` with the following exact JSON schema:
```json
{
  "total_records": 0,
  "unique_normalized_messages": 0,
  "top_message_per_lang": {
    "en": {"normalized_message": "...", "count": 0},
    "ja": {"normalized_message": "...", "count": 0}
  }
}
```

A small sample dataset is available at `/home/user/data/sample_logs.jsonl` for your testing. 

To pass, your Go program must be compiled, and when executed against a massive hidden test file, it must complete extremely quickly (proving you aren't shelling out to the binary) and produce 100% accurate statistics.
You are an automation specialist tasked with fixing a fragile data ingestion pipeline. 

Our company relies on a proprietary log ingestion tool, `/app/bin/log_ingest`, which takes our system logs and indexes them into our data warehouse. Unfortunately, the source code for this tool was lost years ago, and it is highly unstable. It expects logs in a specific line-by-line format:
`[TIMESTAMP] {"key": "value", ...}`

However, the binary frequently crashes (segmentation faults) when processing our real-time log streams due to a bug in its custom JSON-lines parser. Through preliminary debugging, we've noticed it aggressively breaks when it encounters malformed Unicode escape sequences in the JSON payload (e.g., `\u` followed by non-hexadecimal characters or cut off early) or when unescaped literal control characters (ASCII 0x00 to 0x1F) exist in the JSON strings.

Your task is to write a Bash-based streaming pre-processor, `/home/user/filter_stream.sh`, that will sit in front of the `log_ingest` binary to sanitize the data stream.

Your script must:
1. **Stream Processing:** Read from standard input (`stdin`) line-by-line to support indefinitely large streaming files without loading everything into memory. Output to standard output (`stdout`).
2. **Adversarial Filtering:** Identify and completely drop (do not print) any log line that would crash the `log_ingest` binary. You have a copy of the stripped binary at `/app/bin/log_ingest` to test against. You must deduce the exact failure conditions by feeding it inputs or reverse-engineering it. 
3. **Structured Extraction & Normalization:** For all valid lines that are kept, you must extract the `[TIMESTAMP]` prefix and normalize it. The incoming timestamps can be in multiple formats (e.g., `[YYYY/MM/DD HH:MM:SS]` or `[DD-MM-YYYY HH:MM:SS]`). You must convert this prefix to a standard Unix Epoch timestamp enclosed in brackets, e.g., `[1609459200]`. The JSON payload following the timestamp must remain unchanged.

A small sample log file is available at `/app/data/sample.log` for you to inspect the typical structure. You have full access to standard Linux CLI tools (`awk`, `sed`, `grep`, `date`, `jq`, `gdb`, `strings`, `objdump`, etc.).

Ensure your script `/home/user/filter_stream.sh` is executable. The automated test will pipe thousands of clean and "poisoned" lines into your script and pipe your script's output directly into the ingestion tool to verify 100% stability and correct normalization.
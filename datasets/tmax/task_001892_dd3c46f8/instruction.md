You are a log analyst investigating anomalous patterns in system logs. You need to build a robust data processing pipeline in pure Bash to sanitize and validate incoming log files before they are ingested into our data lake. 

You must create a Bash script at `/home/user/process_pipeline.sh` that takes two arguments: an input file path and an output file path.

Your script must implement a pipeline Directed Acyclic Graph (DAG) with the following stages:
1. **Data Masking:** The pipeline must read the input file and mask all Social Security Numbers (format: `XXX-XX-XXXX`, where `X` is a digit). Replace the digits with asterisks, preserving the hyphens (i.e., `***-**-****`).
2. **Quality Gate & Rolling Statistics:** The logs contain a field `BYTES: <number>`. The pipeline must keep a rolling sum of these bytes for every 3 consecutive lines. If the sum of `BYTES` in *any* window of 3 consecutive lines strictly exceeds 1000, this indicates an anomaly. The script must immediately halt, output nothing to the destination file, and exit with status code `1`.
3. **Legacy Obfuscation:** Lines that pass the previous steps must be piped through our proprietary stripped binary located at `/app/legacy_filter`. This binary reads from STDIN, filters out certain blacklisted diagnostic messages, and writes to STDOUT.
4. **Integration:** The final sanitized output must be written to the specified output file, and the script must exit with status code `0`.

Your script must be written entirely in Bash (using shell built-ins, coreutils, awk, sed, etc.). The solution will be tested against two sets of log files: a "clean" set that must be successfully processed and an "evil" set containing anomalies that must be rejected. 

Requirements:
- Your script must be executable (`chmod +x`).
- Expected invocation: `/home/user/process_pipeline.sh <input_file> <output_file>`
- If the rolling sum of bytes in any 3 consecutive lines > 1000, exit 1.
- Otherwise, exit 0 and write the fully processed (masked and filtered) logs to the output file.
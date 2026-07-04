You are a backup administrator tasked with recovering critical system logs from a custom archiving pipeline.

We use a custom tool called `log-archiver` to compress our log directories. The source code for this tool is vendored at `/app/log-archiver-1.0/`. However, the primary script (`/app/log-archiver-1.0/bin/unarchive.sh`) is currently broken due to a bug introduced in the last commit, preventing it from decompressing files correctly. 

Your task consists of two parts:

1. **Fix the Vendored Package:**
   Identify and fix the bug in `/app/log-archiver-1.0/bin/unarchive.sh`. The script is supposed to use `gzip` for decompression, but it appears an environment variable or command reference was mangled. Modify the file in-place so that it functions correctly.

2. **Write a Log Processor:**
   Write a Bash script at `/home/user/process_archive.sh` that takes exactly two arguments:
   `$1`: The path to a custom backup archive file.
   `$2`: A target log severity level (e.g., "ERROR", "WARN", "INFO").

   The backup archive file has the following custom binary/text format:
   - The first 8 bytes contain the ASCII hex representation of the length of the JSON metadata header, followed by a newline (e.g., `0000005A\n`).
   - The next *N* bytes contain the JSON metadata.
   - The remaining bytes are the raw gzipped archive data produced by the `log-archiver` tool.

   Your script must:
   a. Parse the 8-byte length to extract the JSON metadata.
   b. Extract the remaining gzipped payload to a temporary file.
   c. Use the fixed `/app/log-archiver-1.0/bin/unarchive.sh` to extract the payload (it outputs a flat text stream of logs).
   d. Parse the extracted multi-line logs. A log record begins with a timestamp `[YYYY-MM-DD HH:MM:SS]`, followed by the severity `[SEVERITY]`, and then the message which may span multiple lines until the next timestamp.
   e. Output ONLY the complete multi-line log records that match the severity level provided in `$2`.

Your script must print the matching records to standard output, exactly as they appeared in the archive, separated by a single blank line. Ensure your script is executable (`chmod +x /home/user/process_archive.sh`). We will test your script against thousands of generated archive files to verify identical bit-for-bit output.
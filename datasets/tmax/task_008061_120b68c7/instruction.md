You are a storage administrator managing disk space on a critical logging server. The server generates highly repetitive logs, and standard compression tools are too CPU-intensive. You need to implement a custom, line-based Run-Length Encoding (RLE) compression pipeline that safely handles concurrent log archiving.

Your objectives:

1. **Write a Custom Compressor (`/home/user/rle_compress.py`)**
   - Must be written in Python.
   - Reads text from standard input (`sys.stdin`) until EOF.
   - Performs line-based Run-Length Encoding (RLE). For consecutive identical lines, it should count the occurrences.
   - Takes exactly one command-line argument: the path to an output file.
   - Opens the output file in append mode (`a`).
   - Must use `fcntl.flock` to acquire an exclusive lock (`LOCK_EX`) on the output file before writing the fully compressed payload, and release it after writing. This ensures safe concurrent appends.
   - The output format written to the file must be: `<count>|<line_content>` (Note: `<line_content>` already contains a newline at the end, do not add an extra one. If the line was "INFO: system OK\n", output "5|INFO: system OK\n").

2. **Filter and Compress (Bash pipeline)**
   - There are three log files in `/home/user/app_logs/`: `log1.txt`, `log2.txt`, and `log3.txt`.
   - Using `awk` or `sed`, filter out any lines containing the exact string `[DEBUG]`.
   - Pipe the filtered output of each file into your `rle_compress.py` script, appending to `/home/user/archive.rle`.
   - To simulate a concurrent archiving process, run the pipelines in parallel in the background using bash `&` and wait for them to finish using `wait`.
   Example concept (do not copy exactly): `cat file | awk '...' | python3 rle_compress.py archive.rle &`

3. **Verify Archive Integrity (`/home/user/verify.py`)**
   - Write a Python script that reads `/home/user/archive.rle`.
   - Decompresses the RLE format back into raw text.
   - Writes the output to `/home/user/decompressed.txt`.

Ensure all required files (`/home/user/rle_compress.py`, `/home/user/archive.rle`, `/home/user/verify.py`, and `/home/user/decompressed.txt`) are created and populated correctly.
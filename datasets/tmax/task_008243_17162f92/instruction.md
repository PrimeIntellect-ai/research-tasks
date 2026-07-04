You are a storage administrator dealing with a legacy application that is rapidly consuming disk space. The application writes highly repetitive text logs to the directory `/home/user/logs/`. Another process is continuously appending to or reading these logs, so you must process them carefully.

Your task is to write a Bash script at `/home/user/compress_logs.sh` that safely parses and applies a custom Run-Length Encoding (RLE) compression to these log files in place.

Requirements for the script `/home/user/compress_logs.sh`:
1. It must iterate over all `.log` files in `/home/user/logs/`.
2. For each file, it must obtain an exclusive file lock using `flock` on the file to prevent concurrent access issues.
3. It must parse the file's contents. The log files contain various lines, but you only need to compress lines that start exactly with `DATA: ` (the word DATA, a colon, and a space).
4. For the `DATA: ` lines, apply Run-Length Encoding to the data string that follows the space. For example, `DATA: AAAAAAABBBCC` must be converted to `DATA: 7A3B2C`. `DATA: 00000111` must become `DATA: 5031`.
5. Lines that do not start with `DATA: ` (e.g., `INFO:`, `ERROR:`) must be left exactly as they are.
6. To ensure safety, the script must write the processed stream to a temporary file and then atomically replace the original file (using `mv` to overwrite the original).
7. Ensure the script handles standard streams and redirection properly to avoid loading massive files entirely into a single bash variable if possible (using tools like `awk`, `sed`, or bash `while read` loops is permitted).

Once you have written the script, make it executable and run it to compress the existing logs in `/home/user/logs/`.
You are a DevOps engineer debugging a log parsing script that recently started failing. 

There is a Python script at `/home/user/log_parser.py` designed to read `/home/user/server.log` and output a JSON summary. However, the script is currently failing to process the log file due to two distinct bugs:
1. An encoding/serialization issue that causes the script to crash.
2. A bug that causes an infinite loop during tag extraction on certain malformed log lines.

Your task is to debug and fix `/home/user/log_parser.py` according to the following requirements:
- **Encoding Bug:** The log file contains invalid UTF-8 bytes. Modify the script to decode the file using UTF-8, but replace invalid characters with the standard Unicode replacement character (``).
- **Infinite Loop Bug:** The `extract_tags` function gets stuck in a `while` loop when an opening bracket `[` is missing its closing bracket `]`. Fix the logic so that if no closing bracket is found, the remainder of the line (excluding any trailing whitespace/newlines) is extracted as a single tag, and the loop terminates correctly.
- Run the fixed script to generate the output file at `/home/user/parsed_logs.json`.
- Create a text file at `/home/user/debugging_notes.txt` containing exactly two lines:
  - Line 1: The line number in `server.log` (1-indexed) that originally caused the encoding crash.
  - Line 2: The line number in `server.log` (1-indexed) that originally caused the infinite loop.

You must interact with the system to identify the problematic lines, fix the Python code, and produce the requested output files.
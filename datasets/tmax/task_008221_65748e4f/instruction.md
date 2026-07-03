Hello, I'm an IT support technician, and I've been assigned Ticket #8412. We have a Python script that parses logs from one of our containers, but it's failing intermittently depending on the log content. 

The script is located at `/home/user/ticket_8412/parser.py`. It is supposed to read raw text logs from `/home/user/ticket_8412/container_logs.txt` and output JSON-lines to a destination file.

However, when I run:
`python3 /home/user/ticket_8412/parser.py /home/user/ticket_8412/container_logs.txt /home/user/ticket_8412/parsed_logs.jsonl`

It crashes with a `ValueError` on specific log lines. I suspect there is a format parsing edge-case where the log message itself contains characters that confuse the parser.

Please do the following:
1. Use an interactive debugger or print statements to identify which log line is causing the crash and why.
2. Fix the edge-case in `/home/user/ticket_8412/parser.py` so that it correctly extracts the timestamp, log level, and message, even if the message contains square brackets.
3. Run the script successfully to generate `/home/user/ticket_8412/parsed_logs.jsonl`.

The final output file `/home/user/ticket_8412/parsed_logs.jsonl` must contain one valid JSON object per line with the keys `"time"`, `"level"`, and `"message"`.
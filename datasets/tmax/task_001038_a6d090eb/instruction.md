I am an SRE monitoring our internal services. Our log processing pipeline is currently broken due to a recent issue where our Go-based uptime service leaked goroutines under cancellation, occasionally writing incomplete JSON records to our logs before crashing. 

There are two scripts at play:
1. `/home/user/run_processor.sh` - A wrapper script that sets up environment variables and calls our Python processor.
2. `/home/user/process_logs.py` - The script that parses `/home/user/uptime.jsonl`.

Currently, if you run `/home/user/run_processor.sh`, it crashes immediately due to an environment misconfiguration. Even if you fix that, it will crash again when it encounters the incomplete JSON lines in `/home/user/uptime.jsonl`.

Your tasks:
1. Identify and fix the environment misconfiguration in `/home/user/run_processor.sh` (a variable is expected to be a valid integer by the Python script, but it is currently malformed).
2. Modify `/home/user/process_logs.py` so that it handles format parsing edge-cases gracefully. Specifically, if a line cannot be parsed as JSON, the script should catch the error and append the exact unparsed raw line to `/home/user/invalid_logs.txt` (including its trailing newline), rather than crashing. Valid lines should continue to be counted.
3. Create a minimal reproducible example (MRE) script at `/home/user/mre.py`. This script must:
   - Not read from any files.
   - Hardcode one valid JSON string (`'{"url": "site1.com", "uptime": 99}'`) and one specific incomplete JSON string (`'{"url": "site2.com", "uptime": 98'`).
   - Demonstrate the exact same parsing and try/except logic you used in `process_logs.py` to process both strings without raising an unhandled exception.

Run `/home/user/run_processor.sh` and `/home/user/mre.py` to verify your fixes. Leave the fixed files and the generated `/home/user/invalid_logs.txt` in place.
You are an IT Support Technician. We have an open ticket regarding our nightly log aggregation service. 

The service is located at `/home/user/log_processor/`. It uses a Python script (`app.py`) to loop through all customer log files in the `/home/user/log_processor/logs/` directory. For each log file, it calls a Node.js utility (`parser.js`) to parse the custom log format into a JSON string, which the Python script then aggregates.

**The Issue:**
The service crashes intermittently during the nightly run. When it crashes, it dumps a Python traceback about a JSON decoding error and fails to aggregate the remaining logs. The developers believe the issue lies in how `parser.js` parses certain edge-case characters in the log messages, resulting in malformed JSON being passed back to Python.

**Your Tasks:**
1. Run `/home/user/log_processor/app.py` to reproduce the crash and analyze the logging/traceback to identify which specific log file is causing the intermittent failure.
2. Fix the formatting bug in `/home/user/log_processor/parser.js` so it correctly handles edge-case characters (e.g., escaping issues) and outputs valid JSON for all log files. 
3. Run `app.py` again until it successfully processes all logs and generates `/home/user/log_processor/output.json`.
4. Create a resolution report at `/home/user/resolution.txt`. This file must contain exactly two lines:
   - Line 1: The exact filename of the log file that was causing the crash (e.g., `server_01.log`).
   - Line 2: The word `SUCCESS` to indicate the fix is applied.

The automated verification will check for the existence and validity of `/home/user/log_processor/output.json` and the correct identification of the problematic file in `/home/user/resolution.txt`.
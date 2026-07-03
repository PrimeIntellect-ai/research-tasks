You are a performance engineer tasked with investigating a critical livelock issue in a micro-batch telemetry processing system. The worker process occasionally spikes to 100% CPU and stops making progress.

You have been given access to the system where the issue occurred.
Here is the layout of your workspace:
- `/home/user/logs/ingest.log`: Logs from the ingest service. Each line contains a timestamp, a unique record ID, and the raw payload encoded as a hexadecimal string.
- `/home/user/logs/processor.log`: Logs from the C++ worker process. It logs when it starts and finishes processing each record ID.
- `/home/user/src/telemetry_parser.cpp`: The source code for the worker process's parsing logic.

Your objectives:
1. **Log Timeline Reconstruction**: Analyze the logs to identify the specific record ID that caused the worker process to hang (the process started working on it but never finished).
2. **Corrupted Input Handling**: Extract the hex payload for that specific ID and save it as raw binary data to `/home/user/bad_payload.bin`.
3. **Root Cause Analysis & Fix**: The hang is caused by a corrupted input triggering an infinite loop in `telemetry_parser.cpp`. Identify the bug, fix the C++ code so that it gracefully stops processing and returns if the input is corrupted (e.g., if it expects more items than the data contains). 
4. **Recompilation**: Compile the fixed C++ code into an executable at `/home/user/bin/telemetry_parser`.
5. **Reporting**: Create a file at `/home/user/report.txt` with exactly three lines:
   - Line 1: The problematic record ID you identified.
   - Line 2: The raw hex payload string of the problematic record (exactly as it appeared in `ingest.log`).
   - Line 3: The word `FIXED`.

Ensure your compiled executable can process `/home/user/bad_payload.bin` without hanging.
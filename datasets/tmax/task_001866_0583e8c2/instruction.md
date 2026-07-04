You are acting as a Site Reliability Engineer investigating a recent undetected outage. The monitoring dashboard caught the incident, but our log processing pipeline crashed and failed to trigger an alert. 

Your objective involves two main parts:

**Part 1: Video Analysis**
We have a screen recording of the internal status dashboard located at `/app/dashboard.mp4` (a 30 FPS video). You need to find the exact frame number where the main server status indicator changes from "HEALTHY" to "CRITICAL". 
Write only this integer frame number to `/home/user/crash_frame.txt`.

**Part 2: Parser Recovery and Repair**
Our log parsing utility, which triggers the alerts, was recently broken and its source code accidentally deleted from the working tree in `/home/user/uptime_repo`.
1. Recover the deleted parser source code from the Git repository's history. 
2. The recovered parser currently has a format-parsing edge-case bug that causes it to fail or produce incorrect output when processing malformed query results. 
3. You must fix the bug, ensure it compiles/runs, and produce an executable file (or wrapper script) at exactly `/home/user/parser`. You may use any programming language you prefer, as long as the final executable works.

**Parser Requirements:**
The executable `/home/user/parser` must read a single line of raw query log from `stdin` and output the parsed result to `stdout`.
You are provided with a reference oracle binary at `/app/oracle_parser`. Your final `/home/user/parser` must behave **bit-for-bit identically** to `/app/oracle_parser` for *any* input string, including extreme edge cases, invalid formats, and random garbage characters.

Ensure your `/home/user/parser` is executable (`chmod +x`). Once you have created `/home/user/crash_frame.txt` and `/home/user/parser`, your task is complete.
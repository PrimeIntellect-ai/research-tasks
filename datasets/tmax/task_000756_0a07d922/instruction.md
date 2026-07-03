You are a Site Reliability Engineer (SRE) responsible for monitoring service uptime. You rely on a custom, internally built tool to calculate the uptime percentage from ping logs stored in a local database. 

Recently, the monitoring pipeline broke. The source code for the tool is located in a Git repository at `/home/user/uptime_monitor`. 

Here is what you know:
1. The tool currently fails to compile on the `main` branch. 
2. Even before the compilation broke, the previous SRE reported that the tool started outputting wildly incorrect uptime percentages after a recent update, despite the database being unchanged.
3. The uptime logs are stored in an SQLite database located at `/home/user/logs.db` with a single table `ping_results(timestamp INT, status TEXT)`. The `status` is either `'UP'` or `'DOWN'`.

Your task is to:
1. **Fix the build error:** Diagnose the compiler/linker error in the repository and fix it so the tool compiles successfully by running `make`.
2. **Find the regression:** Use `git bisect` (or other git commands) to identify the exact commit hash that introduced the logic bug causing the incorrect uptime calculation.
3. **Debug the query:** Identify what is wrong with the SQL query in the C code and determine the correct query that accurately calculates the number of 'UP' statuses.
4. **Generate a report:** Create a file at `/home/user/debugging_report.txt` containing exactly three lines:
   - Line 1: The full 40-character Git commit hash of the commit that introduced the logical regression.
   - Line 2: The corrected SQL query string needed to properly count the 'UP' statuses (exactly as it should appear inside the `sqlite3_prepare_v2` function string argument).
   - Line 3: The correct uptime percentage for the provided `/home/user/logs.db` database, formatted exactly as the C program prints it (e.g., `Uptime: XX.XX%`).

Constraints:
- You must write your findings to `/home/user/debugging_report.txt` exactly as specified.
- Use standard bash tools, Git, and sqlite3.
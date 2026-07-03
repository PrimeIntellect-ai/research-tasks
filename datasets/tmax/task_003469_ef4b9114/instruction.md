You are acting as a Site Reliability Engineer (SRE). We have a custom C++ daemon that parses service logs to monitor system uptime. Recently, the daemon has been crashing in production when processing specific log formats, and we suspect there are off-by-one errors in the date validation and edge cases in the log format parsing.

Your workspace is located at `/home/user/uptime_monitor`. 

The source code consists of:
- `/home/user/uptime_monitor/parser.cpp`: Contains the parsing logic (`ParseLogLine`).
- `/home/user/uptime_monitor/parser.h`: Header file.
- `/home/user/uptime_monitor/main.cpp`: The main entry point.

Your tasks are to:
1. **Fuzz Testing:** Write a libFuzzer target in `/home/user/uptime_monitor/fuzzer.cpp` that calls the `ParseLogLine` function. Compile it using `clang++ -fsanitize=fuzzer,address -g -O1 fuzzer.cpp parser.cpp -o fuzzer_bin`. Run the fuzzer to identify the crashes.
2. **Debug and Fix:** 
   - There is a boundary condition / off-by-one error related to date parsing (specifically handling month indices and leap years).
   - There is a format parsing edge case where services with spaces in their names (e.g., `WEB SERVER`) cause the parser to incorrectly extract the status code and crash.
   Fix these issues in `parser.cpp`.
3. **Data Transformation & Diffing:** Once fixed, compile the main program (`g++ main.cpp parser.cpp -o uptime_monitor`). Run it against the provided log file `/home/user/uptime_monitor/production.log`.
4. **Output Verification:** The program processes the logs and outputs JSON to standard out. Redirect this output to `/home/user/uptime_report.json`.

Ensure your fixed code doesn't crash on valid edge cases (like leap year dates) and correctly parses service names containing spaces. The final output must be perfectly valid JSON representing the aggregated status counts for each service.
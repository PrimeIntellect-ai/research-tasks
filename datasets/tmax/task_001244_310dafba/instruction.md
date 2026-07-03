You are an infrastructure log analyst investigating a series of anomalies in network activity logs. The logs are provided in JSON-lines format, but our current C++ log ingestion pipeline is breaking down. 

Your task is to build a robust C++ log filter that parses these JSON lines, standardizes the fields, and rigorously validates the data constraints to separate clean logs from malformed or "evil" logs. 

We use a custom, internal JSON parser library located at `/app/vendored/jsonparse-1.2/`. However, there's a problem: the library has a known bug in how it handles Unicode escape sequences (like `\uXXXX`) in JSON strings, causing it to crash or incorrectly parse standard logs. 

Here are your objectives:

1. **Fix the Vendored Package:**
   Investigate the source code of the `jsonparse-1.2` package in `/app/vendored/jsonparse-1.2/`. Find the bug in the Unicode parsing logic (specifically in `src/parser.cpp`) and fix it so it can correctly read 4 hex digits for a `\u` escape sequence. Ensure the package can be compiled.

2. **Develop the Log Filter:**
   Write a C++ program at `/home/user/log_filter.cpp` that utilizes the fixed `jsonparse-1.2` library. Your program should be compiled to `/home/user/log_filter`.
   The program must read JSON-lines from standard input (`stdin`), one line at a time.
   
3. **Feature Extraction, Normalization, and Validation:**
   For each parsed JSON object, perform the following:
   - Extract `timestamp`, `source_ip`, `event_type`, and `bytes_transferred`.
   - **Normalization:** The `bytes_transferred` field is sometimes logged as an integer and sometimes as a string (e.g., `"1042"` or `1042`). Normalize this internally to a standard integer.
   - **Constraint Validation:** 
     - The JSON must be valid and successfully parsed.
     - All four fields (`timestamp`, `source_ip`, `event_type`, `bytes_transferred`) must exist.
     - `source_ip` must follow a basic valid IPv4 format (four integers separated by dots, each 0-255).
     - `bytes_transferred` must be `>= 0`.
   
4. **Output:**
   If a log line passes all validation constraints, print the original, un-modified JSON string to `stdout`. 
   If a log line fails parsing or violates any constraint (an "evil" log), drop it completely (do not print it).

5. **Testing against Corpora:**
   You have been provided with two directories of test logs:
   - `/home/user/logs/clean/`: Contains files with valid log entries. Your program MUST accept and print 100% of these lines.
   - `/home/user/logs/evil/`: Contains files with malformed JSON, invalid constraints, or malicious escape sequences. Your program MUST reject (drop) 100% of these lines.

You can compile your code using `g++ -std=c++17 -I/app/vendored/jsonparse-1.2/include /home/user/log_filter.cpp /app/vendored/jsonparse-1.2/src/parser.cpp -o /home/user/log_filter`. Ensure your final binary strictly adheres to standard input and standard output for its data flow.
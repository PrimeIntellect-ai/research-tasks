I have a large JSON-lines dataset of sensor readings in `/home/user/sensors.jsonl`, but my standard bulk-import tools are crashing because some of the text fields contain malformed Unicode escape sequences. 

I need you to write a C program that streams this data, drops the corrupted records, extracts specific features, and formats the clean data for a database bulk import.

Write a C program at `/home/user/cleaner.c` and compile it to `/home/user/cleaner`. 

The program must:
1. Read lines from `stdin` (simulate large-file streaming, do not load the whole file into memory. Assume max line length is 1024 bytes).
2. Scan each line for malformed Unicode escape sequences. A Unicode escape sequence starts with `\u`. To be valid, it MUST be followed by exactly 4 valid hexadecimal digits (`0-9`, `a-f`, `A-F`). If a `\u` is followed by anything else (or the string ends before 4 characters), the line is considered corrupted.
3. For every corrupted line, write the 1-based line number followed by a newline to a pipeline monitoring log at `/home/user/error.log`. Skip processing this line.
4. For valid lines, extract the integer value of `"event_id"` and the float value of `"sensor_val"`. You can assume the JSON for valid lines will strictly contain `"event_id": <int>` and `"sensor_val": <float>` (with a single space after the colon) somewhere in the line.
5. Print the extracted features to `stdout` in CSV format: `event_id,sensor_val` (e.g., `105,42.500000`).

After writing and compiling the program, run it by piping `/home/user/sensors.jsonl` into it, and redirect the output to `/home/user/clean_data.csv`.

Ensure your C program is robust and exactly follows the logging and output formatting rules.
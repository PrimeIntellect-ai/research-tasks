You are a data analyst managing a time-series data pipeline. We use a proprietary, highly optimized but fragile feature extraction tool located at `/app/legacy_ts_parser`. This tool processes CSV files containing sensor readings, but it has a major flaw: it crashes (often segfaulting) if it encounters malformed character encodings, specifically invalid UTF-8 byte sequences or unexpected null bytes in the `sensor_name` column.

Your task is to build a robust C++ filter that acts as a gatekeeper in our pipeline DAG, preventing malicious or corrupted files from crashing the legacy parser. 

**Requirements:**
1. Write a C++ program at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
2. The program must take a single command-line argument: the path to a CSV file.
3. It must read the CSV file (`timestamp,sensor_name,value`) and validate the character encoding:
   - Every byte in the file must be valid UTF-8.
   - There must be no null bytes (`\0`) anywhere in the file.
   - The file must not contain ASCII control characters (bytes `0x00` to `0x1F`), EXCEPT for standard whitespace (`\t` `0x09`, `\n` `0x0A`, `\r` `0x0D`).
4. **Behavior on Clean Files:** If the file strictly adheres to these rules, print exactly `CLEAN` to standard output and exit with code `0`.
5. **Behavior on Corrupted/Evil Files:** If the file violates any rule, print exactly `REJECT` to standard output and exit with code `1`.

We have provided a few sample files in `/home/user/samples/` for you to test your program, as well as the `/app/legacy_ts_parser` binary which you can use as a black-box oracle to see what inputs cause a crash.

To complete the task, ensure the compiled binary `/home/user/sanitizer` is ready. An automated system will invoke your program against a large batch of hidden test files.
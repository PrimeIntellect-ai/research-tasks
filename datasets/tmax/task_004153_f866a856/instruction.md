You are an AI assistant acting as a storage administrator for a large Linux-based web service. Your log partition is constantly running out of space because of bloated application logs.

The logs are written as JSONLines (one JSON object per line). You need to build a C program to sanitize these logs by filtering out "bloated" entries, and integrate it with a file-watching script to process new logs as they arrive.

Part 1: Fix the Vendored Package
We use `cJSON` for JSON parsing. Its source is vendored at `/app/cJSON`. However, the previous admin broke the Makefile, so it currently fails to build.
1. Inspect and fix the `Makefile` in `/app/cJSON`.
2. Build the package so `libcjson.a` and `libcjson.so` are produced.

Part 2: Write the Log Sanitizer in C
Write a C program at `/home/user/log_sanitizer.c` that uses the compiled `cJSON` library. 
1. The program must accept exactly two arguments: `./log_sanitizer <input_file> <output_file>`
2. It should read `<input_file>` line by line.
3. It must parse each line as JSON.
4. If the JSON object contains a key named `"core_dump"`, the line is considered "evil" (bloated) and MUST NOT be written to the output.
5. If the JSON object does NOT contain `"core_dump"`, it is "clean" and MUST be written to the output exactly as it appeared (do not re-format the JSON; output the original string).
6. **Atomic Writes:** To prevent incomplete files from being read by log forwarders, your program must write the accepted lines to `<output_file>.tmp`. Once all processing is complete and the file is closed, you must atomically rename it to `<output_file>`.

Part 3: Verify the Sanitizer
There are two corpora of log files provided for testing:
- `/app/corpora/evil/`: Contains logs where every line has a `"core_dump"` key.
- `/app/corpora/clean/`: Contains normal log files.
Your compiled program must drop 100% of the evil entries and preserve 100% of the clean entries.

Part 4: Automation
Write a bash script at `/home/user/watch_logs.sh` that uses `inotifywait` to monitor the directory `/var/spool/incoming_logs/` for new files (specifically the `CLOSE_WRITE` event).
When a new file is detected, it should automatically run your `log_sanitizer` to output the sanitized file into `/var/log/sanitized_logs/` with the same filename.

Requirements:
- Compile your C program to `/home/user/log_sanitizer`.
- Ensure your bash script is executable.
- Leave the bash script running in the background.
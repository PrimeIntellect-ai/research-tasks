You are a performance engineer tasked with debugging a custom Python profiling script. 

The script `/home/user/profiler.py` is designed to read and aggregate JSON system trace files from the directory `/home/user/traces/`. However, the script is currently failing to complete its run.

Your task is to fix `/home/user/profiler.py` by addressing the following issues:
1. **Resource Leak / OS Error:** The script currently crashes before processing all files due to an operating system level error. You may use standard debugging tools (like tracebacks or system call tracing tools like `strace`) to identify the issue. Fix the script so it correctly manages system resources and can process all files.
2. **Corrupted Input Handling:** Some trace files contain corrupted, invalid JSON. Modify the script to catch JSON parsing errors gracefully. Instead of crashing, the script must append the exact filename of any corrupted file (e.g., `trace_123.json`) to a log file located at `/home/user/corrupt_files.txt`.
3. **Assertion-based Validation:** Even if the JSON is valid, some trace files might be missing the required `cpu_util` key. Immediately after parsing a valid JSON file, add an assertion to validate this intermediate state: `assert "cpu_util" in data, f"Missing cpu_util in {filepath}"`. Catch this `AssertionError`, and append the filename of the offending file to `/home/user/missing_keys.txt`.

Ensure the script completes its execution successfully (exit code 0) after your fixes, and that the two output text files (`/home/user/corrupt_files.txt` and `/home/user/missing_keys.txt`) correctly list the problematic files, one per line. Do not change the final print statement that outputs the total aggregated CPU usage.
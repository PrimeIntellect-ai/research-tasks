A long-running data processing service written in C is experiencing an elusive memory leak. We have captured a large historical payload that triggers the leak, but we need to isolate the exact sequence of events that causes it to prevent future occurrences.

You are provided with:
1. The source code of the service at `/home/user/service.c`
2. The compiled binary at `/home/user/service`
3. A large input file at `/home/user/input.txt` containing a sequence of integer payloads (one per line). When fed into the service via standard input, it triggers the memory leak.

Your task is to:
1. **Minimize the Test Case:** Identify the precise, minimal contiguous sequence of inputs (consecutive lines) from `input.txt` that triggers the memory leak. Write these exact integers, one per line, to `/home/user/minimal_leak.txt`.
2. **Construct a Regression Test:** Create a bash script at `/home/user/test_leak.sh` that takes a single file path as an argument. The script should run the compiled service against the provided file under `valgrind` and exit with status code `1` if a memory leak (definitely lost bytes > 0) is detected, and exit with status code `0` if no leak is detected. Ensure the script is executable.

Note:
- You should use standard Linux CLI tools (e.g., `valgrind`, `head`, `tail`, `grep`, `bash` loops) to isolate the leak. 
- The minimal sequence is the smallest number of consecutive lines from the original input that, when fed to the program, causes a leak.
You are an open-source maintainer reviewing a pull request. A contributor has attempted to rewrite a legacy data processing utility in Python. The legacy utility is provided as a stripped, compiled binary located at `/app/legacy_processor`.

The tool reads JSON lines from standard input, performs a custom transformation involving interval math, and writes the results as JSON lines to standard output. 

The contributor's PR code is located at `/home/user/processor.py`. They attempted to port the legacy tool to Python, specifically mimicking Go concurrency patterns (using thread pools and queues similar to goroutines and channels) to process the lines concurrently, and using a custom data structure to merge overlapping intervals.

However, the PR is broken:
1. It frequently hangs/deadlocks and doesn't terminate when the input stream ends.
2. The custom interval merging logic is incorrect.
3. It occasionally drops lines or misformats the output JSON.

Your task is to fix `/home/user/processor.py`. You should treat `/app/legacy_processor` as a black-box oracle to determine the exact expected input/output behavior (what fields it expects, how it calculates the interval span, and how it formats the output). 

Requirements:
- Fix the concurrency/queueing bugs so the script processes all inputs and terminates cleanly when EOF is reached.
- Fix the custom interval merging logic to perfectly match the legacy binary's output.
- The fixed Python script must be fully functionally equivalent (bit-exact standard output) to the legacy binary for any valid sequence of JSON lines.
- Do not change the file path; keep the fixed code at `/home/user/processor.py`.
- Ensure it reads from `sys.stdin` and writes to `sys.stdout`.
You are a performance engineer analyzing a mathematical computation service. The service computes prime numbers and logs its progress. Recently, the binary has been crashing due to a segmentation fault. To make matters worse, a buggy cleanup script deletes the log file immediately upon program exit, meaning we lose the log data right when the crash happens.

We have the source code for the application at `/home/user/prime_cruncher.c`.

Your task is to:
1. Compile the C code with debugging symbols enabled (`-g`) into an executable named `/home/user/prime_cruncher`.
2. Run the application in a debugger (like `gdb`) to trigger the crash and analyze the state.
3. Identify the exact name of the C function that directly causes the segmentation fault.
4. The application allocates a heap buffer (`log_buffer`) that acts as an in-memory log before flushing. Since the actual log file is deleted, you must recover the log data directly from the program's memory state at the time of the crash.
5. Inspect the `log_buffer` string in memory to find:
   a. The value of the very last "Calculated Prime" logged before the crash.
   b. The secret `sequence_id` appended to the log buffer right before the crash.

Create a report file at `/home/user/debug_report.txt` with exactly the following three lines (replace the bracketed placeholders with your findings):

```
Crashing Function: [function_name]
Last Prime: [number]
Sequence ID: [id]
```
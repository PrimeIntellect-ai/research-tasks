You are a Linux Systems Engineer tasked with hardening the configuration monitoring of a sensitive environment. Our vendor has provided a proprietary, pre-compiled filesystem event logger located at `/app/bin/fs_event_gen`. 

When executed, this binary simulates capturing filesystem events and writes them to a binary log file. We need to continuously monitor these logs for unauthorized modifications to configuration files. 

Your task is to build a high-performance filtering pipeline using C and shell scripting.

**Step 1: Understand the Data Source**
The binary `/app/bin/fs_event_gen` takes two arguments: a seed (integer) and an output file path. 
Example: `/app/bin/fs_event_gen 42 /home/user/events.bin`
This will generate a large binary log file. The binary format consists of sequential records without any padding between them. Each record has the following header:
- an 8-byte unsigned integer (timestamp)
- a 4-byte unsigned integer (event type)
- a 2-byte unsigned integer (path length)
Immediately following the header is the file path string (not null-terminated) of `path length` bytes.

**Step 2: Develop a High-Performance Filter in C**
Write a C program at `/home/user/fast_filter.c` that reads the binary log file specified as its first command-line argument.
Your program must:
1. Parse the records efficiently.
2. Filter for events where the `event type` is exactly `3` (which corresponds to an IN_MODIFY event on our systems).
3. Further filter the results to only include paths that end with the exact suffix `.conf`.
4. Print the matching file paths to standard output, one per line (add a newline after each path).

Because the event logs in production are massive, performance is critical. Your C program must process a 500MB log file in an extremely short time. You are encouraged to use memory-mapped IO (`mmap`) or large buffer reads (`fread`) and compiled with high optimization levels (`-O3`). A naive byte-by-byte read will fail our performance threshold.

**Step 3: Create a CI/CD Build and Benchmark Script**
Create a script at `/home/user/build_and_test.sh` that automates your build and validation process:
1. Compile `/home/user/fast_filter.c` to an executable at `/home/user/fast_filter` with maximum optimizations.
2. Generate a test log by executing `/app/bin/fs_event_gen 100 /home/user/test_events.bin`.
3. Execute your compiled program against `/home/user/test_events.bin`, redirecting standard output to `/home/user/filtered.log`.

Make sure `/home/user/build_and_test.sh` is executable.

You may run the generator and your scripts as many times as you need to debug and optimize your C code. When you are finished, ensure the final script `/home/user/build_and_test.sh` exists and successfully produces the `/home/user/filtered.log` output.
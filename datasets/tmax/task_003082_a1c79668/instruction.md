You are acting as a support engineer collecting diagnostics and fixing a tool. We have a legacy stripped binary located at `/app/bin/query_formatter` that processes query result logs. Unfortunately, this binary frequently deadlocks under high contention in our multithreaded pipeline, causing severe bottlenecks.

Your task is to reverse-engineer the behavior of this binary and reimplement it perfectly as a pure Bash script at `/home/user/formatter.sh`. 

You should use tools like `strace`, `ltrace`, or run black-box input/output diff analysis to determine exactly how the binary transforms input data. 

Requirements for your Bash script:
1. It must read from standard input and write to standard output.
2. It must produce BIT-EXACT the same output as the original binary for any valid input.
3. It must be written in Bash (`#!/bin/bash`).
4. Make sure your script is executable.

You do not need to reproduce the deadlock—in fact, your Bash script will serve as the deadlock-free replacement in our pipeline.
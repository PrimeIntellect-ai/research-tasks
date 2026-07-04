You are a DevOps engineer responding to an urgent incident. We have a legacy system that normalizes and deduplicates incoming application logs. As part of the pipeline, log lines are piped through a proprietary, compiled utility located at `/app/log_hasher`. This utility calculates a proprietary hash for each log line.

Unfortunately, we lost the source code for `/app/log_hasher` years ago. Recently, it has started segmentation faulting on extremely long log lines, causing pipeline bottlenecks. We need to replace it with a robust Python implementation.

Your task is to:
1. Reverse engineer the stripped binary `/app/log_hasher`. You can use any tools available (e.g., `objdump`, `strings`, `gdb`, `strace` or Python scripts) to understand its hashing algorithm. The binary reads lines from `stdin`, processes them, and outputs an 8-character hexadecimal string for each line to `stdout`.
2. Create a minimal reproducible example and test suite. Write a script `generate_test_logs.py` that creates various edge-case log lines, and a regression test `test_parser.py` that verifies your Python implementation's outputs match the legacy binary's outputs exactly.
3. Implement the exact hashing algorithm in Python. Write the final script to `/home/user/log_parser.py`. This script must read lines from standard input (`sys.stdin`), compute the identical hash for each line, and print the hex string to standard output (`sys.stdout`), perfectly mimicking the legacy binary.

Ensure your Python script handles strings correctly and matches the bitwise operations of the original binary precisely. The automated verifier will randomly fuzz your `/home/user/log_parser.py` against the original `/app/log_hasher` with thousands of inputs to ensure bit-exact equivalence.
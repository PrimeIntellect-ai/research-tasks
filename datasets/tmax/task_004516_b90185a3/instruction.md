I need your help debugging a regression in a database recovery and timeline reconstruction tool. 

The source code for the tool is provided as a vendored git repository at `/app/wal_processor`. It is a Python package that reads write-ahead log (WAL) files from multiple services concurrently, reconstructs the timeline of events, and recovers the final database state.

Recently, a regression was introduced somewhere in the last 200 commits that causes a race condition during concurrent log parsing, leading to corrupted recovered states (missing or incorrectly ordered events). The `main` branch currently has this bug.

Your task:
1. Use `git bisect` (or manual analysis) in `/app/wal_processor` to find the exact commit that introduced the race condition. 
2. Analyze the root cause of the concurrency bug (e.g., shared mutable state, improper locking, or thread-unsafe operations in the worker pool).
3. Fix the bug on the `main` branch.
4. After fixing the bug, create a standalone entry point for your fixed program at `/home/user/fixed_processor.py`. This script should take a single command-line argument (the path to a directory containing WAL files) and print the recovered JSON state to standard output.

The output of `/home/user/fixed_processor.py <wal_dir>` must be completely deterministic and bit-exact equivalent to our reference oracle, which is located at `/app/oracle_processor`. The oracle correctly processes the files without the race condition.

Ensure your fixed script is executable and outputs exactly what the oracle outputs for any valid directory of WAL logs.
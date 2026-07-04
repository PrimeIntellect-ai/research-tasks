You are tasked with replacing a legacy backup utility for our database system. The legacy tool, located at `/app/wal_scanner` (a stripped binary), parses proprietary Write-Ahead Log (WAL) files and outputs a CSV summary of transaction metadata. 

However, `/app/wal_scanner` is extremely slow and cannot keep up with our log rotation script that continuously archives logs. Your goal is to write a highly optimized replacement in C++ that produces the exact same output but is significantly faster.

You have been provided a sample WAL file at `/home/user/sample.wal`. 

Instructions:
1. Reverse-engineer the WAL file format and the aggregation logic used by `/app/wal_scanner`. You can analyze the binary, run it against the sample, or craft your own WAL files to fuzz the oracle and understand the format.
2. Write a C++ program at `/home/user/fast_scanner.cpp`.
3. Compile it to `/home/user/fast_scanner` (e.g., using `g++ -O3`).
4. Your program must accept a single command-line argument (the path to a WAL file) and print the resulting CSV to `stdout`.
5. The output must be perfectly identical to the output of `/app/wal_scanner` for any valid WAL file.
6. Your program must be highly optimized.

Your implementation will be evaluated against a hidden, large WAL file. To succeed, your program's output must exactly match the legacy binary's output, and your program must achieve a runtime speedup of at least 5.0x compared to the legacy binary.
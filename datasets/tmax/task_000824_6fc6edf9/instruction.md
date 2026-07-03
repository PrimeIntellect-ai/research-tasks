You are acting as a data analyst working on database concurrency issues. We need a tool to process CSV logs of transaction waits to detect potential deadlocks (cycles in the wait-for graph).

You have been provided with a vendored C++ CSV parsing library located at `/app/csv-parser`. However, the previous engineer left it in a broken state—it currently fails to compile when included in a modern C++ project due to a misconfigured build or environment file within its directory.

Your task is to:
1. Identify and fix the perturbation in the `/app/csv-parser` package so it can be used.
2. Write a C++ program at `/home/user/deadlock_detector.cpp` that uses this library to read a wait-for graph from a CSV file.
3. The CSV file will have two columns with a header: `tx_id,waiting_for_tx_id`. Each row indicates that transaction `tx_id` is waiting on a lock held by `waiting_for_tx_id`.
4. Your program must materialize this as a directed graph and determine if a deadlock (a cycle) exists.
5. Compile your program to an executable named `/home/user/deadlock_detector`.
6. The executable must take exactly one command-line argument: the path to the CSV file to analyze.
   - If NO cycle is found (safe), the program must exit with status code `0`.
   - If ANY cycle is found (deadlock), the program must exit with status code `1`.

Example invocation:
`/home/user/deadlock_detector /home/user/sample.csv`

Ensure your executable handles all standard cases of directed cycle detection.
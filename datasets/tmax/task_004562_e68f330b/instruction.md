You are a data engineer at a database infrastructure company. We are analyzing transaction wait-for graphs exported as CSV files to detect deadlocks.

Currently, we rely on a proprietary, legacy deadlock detection engine provided as a stripped, UPX-packed binary at `/app/deadlock_detector`. This binary takes a path to a CSV file and exits with code `1` if a deadlock (cycle) is detected, and `0` if the graph is safe. Unfortunately, this binary is extremely slow and we cannot inspect its source code. 

Your task is to write a highly optimized C++ program that exactly replicates the deadlock detection logic of the legacy binary.

**Data Format:**
You are analyzing CSV files with the following structure (no header):
`transaction_id,resource_id,lock_status`
- `transaction_id`: Integer
- `resource_id`: Integer
- `lock_status`: String, either `HELD` or `WAITING`

**Graph Semantics:**
You will need to reverse-engineer the exact rules of how the binary constructs the "wait-for" graph and detects deadlocks by passing it test CSVs. As a hint: deadlocks occur when transactions are caught in a circular dependency waiting for resources held by other transactions.

**Requirements:**
1. Write your C++ source code to `/home/user/detector.cpp`.
2. Compile it to `/home/user/detector`.
3. Your compiled program must accept a single command-line argument (the path to the CSV file).
4. Your program must exit with code `1` if a deadlock is detected (reject), and code `0` if no deadlock is detected (accept).
5. It must flawlessly agree with `/app/deadlock_detector` on any valid CSV input.

We will test your binary against a hidden corpus of clean and deadlocked CSV graphs. Ensure your graph traversal and cycle detection algorithms are highly efficient.
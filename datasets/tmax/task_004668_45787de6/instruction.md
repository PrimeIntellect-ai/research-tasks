You are acting as a technical compliance officer auditing a database system's transaction manager. We suspect that certain concurrent transactions are experiencing deadlocks due to acquiring locks on the same resources in reverse order. 

You have been provided with a transaction lock log file at `/home/user/tx_logs.csv`. The file is a comma-separated text file with no header. Each line represents a lock acquisition in the format:
`timestamp,transaction_id,resource_id`
(All values are positive integers. The file is sorted chronologically by timestamp).

Your task is to write a C program named `/home/user/detect.c` that acts as a custom query engine to find potential deadlock cycles.

Requirements for the C program:
1. Parse `/home/user/tx_logs.csv`.
2. Build an efficient in-memory index to track the sequence of resources locked by each `transaction_id`.
3. Detect all unique pairs of transactions `(T_A, T_B)` and resources `(R_X, R_Y)` such that:
   - `T_A` locks `R_X` and later locks `R_Y`.
   - `T_B` locks `R_Y` and later locks `R_X`.
   - To avoid duplicate pairs, ensure `T_A < T_B` and `R_X < R_Y`.
4. Sort the detected deadlock pairs primarily by `T_A` ascending, then by `T_B` ascending.
5. The program must accept two command-line arguments for pagination (filtering): `<limit>` and `<offset>`. It should output only the records starting from `offset` (0-indexed) up to `limit` records.
6. The output format for each line must be exactly: `T_A,T_B,R_X,R_Y`

Once you have written and compiled the C program to `/home/user/detect`, use standard bash shell commands to execute the following pipeline query:
Run your program to fetch a paginated result with a `limit` of 5 and an `offset` of 1 (i.e., skipping the very first detected deadlock pair). Pipe the output of your program directly into a file located at `/home/user/audit_report.txt`.

Ensure your C code compiles cleanly with `gcc /home/user/detect.c -o /home/user/detect` without requiring any external libraries beyond the standard C library.
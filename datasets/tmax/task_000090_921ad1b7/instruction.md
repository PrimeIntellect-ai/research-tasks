You are a Database Reliability Engineer (DRE) investigating a major system stall that occurred during the nightly backup window. Several backup processes and standard transactions have completely frozen. You suspect a deadlock caused by complex circular dependencies.

I have exported the current lock state of the database into two CSV files:
1. `/home/user/held_locks.csv`: Contains locks currently granted. The columns are `pid,table_name`.
2. `/home/user/waiting_locks.csv`: Contains lock requests that are currently blocked. The columns are `pid,table_name`.

Your task is to:
1. Construct a "wait-for" graph based on this data. A process `P_A` is considered to be "waiting for" process `P_B` (a directed edge `P_A -> P_B`) if `P_A` is waiting for a lock on a table that `P_B` currently holds.
2. Identify the deadlock. The deadlock will manifest as a directed cycle in this wait-for graph. (There is exactly one distinct cycle in the provided data).
3. Extract the exact sequence of process IDs (PIDs) involved in this cycle.
4. Output this sequence to a file named `/home/user/deadlock.txt`. 

Formatting rules for `/home/user/deadlock.txt`:
- The file must contain a single line of comma-separated PIDs (no spaces).
- The sequence must start with the lowest PID present in the cycle.
- The sequence must follow the direction of the wait-for edges (i.e., if PID 10 waits for PID 20, 20 should follow 10).
- Do not repeat the starting PID at the end. (e.g., if the cycle is 10->20->30->10, output `10,20,30`).

You may write a script in any language available in the standard environment (like Python, Bash, AWK) to compute this. Do not install heavy external graph databases; write standard code to traverse the dependencies.
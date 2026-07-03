You are acting as a compliance officer auditing a legacy banking system. We have detected a system freeze, and suspect a transaction deadlock (circular dependency) caused by concurrent processes waiting on each other's locked resources.

Your task is to write a Bash script that reverse-engineers the transaction data model from flat log files, constructs a dependency graph, and performs a recursive graph traversal to find the deadlock cycle.

We have a lock table dump located at `/home/user/transaction_locks.csv`.
The CSV has no header and follows this format:
`TRANSACTION_ID,RESOURCE_ID,LOCK_STATUS`
(LOCK_STATUS is either `GRANTED` or `WAITING`).

A dependency occurs when Transaction A is `WAITING` on a Resource that is currently `GRANTED` to Transaction B. This means Transaction A depends on Transaction B.

Write a script at `/home/user/detect_cycle.sh` that:
1. Takes exactly one argument: the starting `TRANSACTION_ID`.
2. Reads `/home/user/transaction_locks.csv`.
3. Recursively chains the dependencies to find a deadlock cycle starting from the given transaction.
4. Outputs the deadlock cycle to exactly `/home/user/deadlock_report.txt` in the format: `T_START -> T_NEXT1 -> T_NEXT2 -> ... -> T_START`
5. Uses strictly Bash built-ins and standard coreutils (e.g., awk, grep, sed). Do not use Python, Perl, or any external scripting languages.

For example, if T1 waits for a resource held by T2, and T2 waits for a resource held by T1, the output for starting transaction T1 should be:
`T1 -> T2 -> T1`

Run your script with the starting transaction `TX_994` to generate the `/home/user/deadlock_report.txt` file. Make sure your script handles execution permission correctly.
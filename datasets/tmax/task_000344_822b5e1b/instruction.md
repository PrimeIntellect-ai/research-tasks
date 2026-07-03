You are acting as a compliance officer auditing a financial database system. Recently, the system has experienced severe slowdowns, and we suspect concurrent transactions are getting stuck in deadlocks.

I have exported the raw database lock request logs to `/home/user/lock_events.csv`. 
The CSV has the following format:
`Timestamp,Status,WaitingTxID,HoldingTxID,ResourceName`

Your task is to build a data pipeline and a C program to detect which transactions are deadlocked (i.e., involved in a cyclic wait dependency) and generate a paginated audit report.

Perform the following steps:
1. Write a bash script `/home/user/build_and_run.sh` that orchestrates the entire process.
2. The script must first use standard shell tools (like `grep`, `awk`, etc.) to filter `/home/user/lock_events.csv` to include ONLY rows where the `Status` is exactly `WAITING`. 
3. The script must extract the `WaitingTxID` and `HoldingTxID` from these filtered rows and pipe them into a C program.
4. Write a C program at `/home/user/detect_cycles.c` (compiled to `/home/user/detect_cycles` by your script). The program should read pairs of integers (`WaitingTxID` and `HoldingTxID`) from standard input.
5. The C program must materialize this data as a directed graph (where an edge from Waiter to Holder means the Waiter is waiting on the Holder) and find ALL transaction IDs that are part of at least one cycle (deadlock). It should print these deadlocked transaction IDs to standard output, one per line.
6. Your bash script should take the output of the C program, sort the transaction IDs numerically in **descending** order, and filter/paginate it to keep ONLY the **top 4** highest transaction IDs.
7. The final 4 transaction IDs must be saved to `/home/user/audit_report.txt`, one ID per line.

Ensure your `build_and_run.sh` is executable and runs the compilation and the full pipeline when executed.
You are a Database Administrator tasked with investigating a series of transaction deadlocks that brought down our production system. We managed to export the raw lock events into an SQLite database file located at `/home/user/syslogs.db`. Unfortunately, the documentation for the schema was lost, so you will need to reverse-engineer the data model first.

Your objective is to write a bash script at `/home/user/find_deadlocks.sh` that queries this database to find all occurrences of classic two-way deadlocks and outputs the results.

A two-way deadlock in this system is defined as:
1. Transaction A successfully acquired a lock on Resource X.
2. Transaction B successfully acquired a lock on Resource Y.
3. Transaction A subsequently started waiting for a lock on Resource Y.
4. Transaction B subsequently started waiting for a lock on Resource X.
(Assume neither transaction released their acquired locks before waiting).

Your bash script must execute an SQLite query (or multiple) against `/home/user/syslogs.db` and output the detected deadlocks to a CSV file at `/home/user/deadlocks.csv`.

The output CSV must:
1. Have no header row.
2. Contain exactly four columns: `txn_1`, `txn_2`, `resource_1`, `resource_2`.
3. Ensure that `txn_1` is alphabetically less than `txn_2` (e.g., if T1 and T2 deadlock, T1 is `txn_1`).
4. `resource_1` should be the resource that `txn_1` acquired first and `txn_2` is waiting on. `resource_2` should be the resource `txn_2` acquired first and `txn_1` is waiting on.
5. Be sorted ascending by `txn_1`, then `txn_2`.

Use standard bash and `sqlite3` commands. Ensure your script is executable. Run your script to generate the final `/home/user/deadlocks.csv` file so I can verify the results.
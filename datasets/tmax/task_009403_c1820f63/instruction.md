You are acting as a compliance officer performing a system audit on a transactional database. You suspect there is a transaction deadlock occurring due to a cyclic lock dependency. 

You have been provided with two CSV files containing the current lock table state:
1. `/home/user/held_locks.csv` - Contains locks currently held by transactions. Format: `resource_id,transaction_id`
2. `/home/user/requested_locks.csv` - Contains locks requested by transactions that are currently blocked. Format: `transaction_id,resource_id`

Your task is to:
1. Map the relationships between these files to build a "waits-for" graph (i.e., Transaction A is waiting for a resource held by Transaction B).
2. Traverse this graph using only Bash tools (`awk`, `join`, `grep`, etc.) to find a deadlock. A deadlock in this scenario is defined as a cycle of exactly 3 transactions (e.g., Tx1 waits for Tx2, Tx2 waits for Tx3, and Tx3 waits for Tx1).
3. Identify the three `transaction_id`s involved in this 3-cycle deadlock.
4. Output the three `transaction_id`s in ascending alphabetical order, separated by commas (e.g., `T001,T002,T003`), and save this exact string to `/home/user/deadlock_report.txt`.

Constraints:
- Use only standard Linux shell tools and built-ins (Bash, awk, sed, grep, join, sort, etc.). Do not use Python, Perl, or any database engines.
You are a data analyst tasked with analyzing database transaction logs to identify deadlocks. You have been provided with a CSV file `/home/user/data/locks.csv` which contains information about resource locks.

The file `/home/user/data/locks.csv` has the following header and columns:
`tx_id,resource_id,status,timestamp`
- `tx_id`: The ID of the transaction (e.g., T1, T2)
- `resource_id`: The ID of the resource being locked (e.g., R1, R2)
- `status`: Either `GRANTED` (meaning the transaction holds the lock on the resource) or `WAITING` (meaning the transaction is blocked, waiting to acquire the lock).
- `timestamp`: An integer representing the time the event occurred.

A deadlock of size 2 occurs between two transactions, `tx_A` and `tx_B`, when:
1. `tx_A` is `WAITING` on `resource_X`, which is currently `GRANTED` to `tx_B`.
2. `tx_B` is `WAITING` on `resource_Y`, which is currently `GRANTED` to `tx_A`.

Your task is to write a bash script at `/home/user/find_deadlocks.sh` that processes `locks.csv` and finds all such deadlocked pairs. You must use standard Linux shell utilities (like `awk`, `join`, `sort`, `grep`)—do not use Python, Perl, or other scripting languages.

The script must generate a report at `/home/user/deadlocks_report.csv` with the exact following header:
`tx_1,tx_2,resource_1,resource_2`

For each deadlock pair found, append a row where:
- `tx_1` is the transaction ID of the first transaction.
- `tx_2` is the transaction ID of the second transaction.
- `tx_1` must be strictly less than `tx_2` (using standard lexicographical string comparison, e.g., "T1" < "T2").
- `resource_1` is the resource that `tx_1` is `WAITING` on.
- `resource_2` is the resource that `tx_2` is `WAITING` on.

Sort the final data rows (excluding the header) by `tx_1` ascending, then by `tx_2` ascending.

To complete the task, your script must be runnable via `bash /home/user/find_deadlocks.sh` and successfully produce the correct `/home/user/deadlocks_report.csv`.
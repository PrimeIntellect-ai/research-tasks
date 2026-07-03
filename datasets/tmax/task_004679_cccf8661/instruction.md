You are a compliance officer performing a system audit on a transactional database. We suspect that several concurrent transactions have entered a deadlock state. 

We have extracted the "wait-for" logs into a relational format in a CSV file located at `/home/user/transactions.csv`. The CSV has no header and contains two columns: `tx_id` and `waiting_for_tx_id`. Every row represents a directed edge indicating that `tx_id` is blocked waiting for `waiting_for_tx_id` to release a lock.

Your task is to write a Rust program to analyze this data:
1. Create a Rust project or standalone script in `/home/user/audit_deadlocks`.
2. The compiled binary must accept exactly three positional command-line arguments: `<csv_path> <limit> <offset>`. (e.g., `./audit_deadlocks transactions.csv 5 2`).
3. The program must read the relational CSV data and map it into an in-memory Graph representation.
4. It must traverse the graph to find **all** transaction IDs (`tx_id`) that are part of at least one cycle (a deadlock). Transactions that merely point to a cycle but are not part of the closed loop themselves should NOT be included.
5. Extract the unique set of deadlocked transaction IDs, sort them numerically in ascending order.
6. Apply the pagination parameters: skip the first `<offset>` elements and take up to `<limit>` elements.
7. Write the resulting transaction IDs (one per line) to `/home/user/deadlocked_txs.txt`.

Once you have written and compiled the program, run it with the following arguments:
Limit: `4`
Offset: `3`
Targeting the provided `/home/user/transactions.csv` file.

The final state must contain the correctly paginated list of deadlocked transaction IDs in `/home/user/deadlocked_txs.txt`.
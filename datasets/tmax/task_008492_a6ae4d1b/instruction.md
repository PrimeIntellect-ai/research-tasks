You are a Database Reliability Engineer (DBRE) investigating a severe performance degradation. You suspect a deadlock is causing a pile-up of transactions in the database. 

A monitoring tool has dumped the current lock waits into a JSON file located at `/home/user/transactions.json`. This file contains an array of transaction objects. Each object has the following schema:
- `tx_id` (integer): The unique identifier of the transaction.
- `waiting_for_tx` (integer or null): The `tx_id` of the transaction that this transaction is waiting on. If it is not waiting for any transaction, this value is `null`.
- `duration` (integer): The number of seconds the transaction has been active.
- `query` (string): A snippet of the SQL query being executed.

Your task is to write a Go program at `/home/user/analyze.go` that performs the following steps:
1. Parse the `/home/user/transactions.json` file.
2. Treat the data as a directed "waits-for" graph, where a directed edge exists from `tx_id` to `waiting_for_tx`.
3. Traverse the graph to detect a deadlock. A deadlock is defined as a cycle in this directed graph. Assume there is exactly one cycle in the provided data. Find all `tx_id`s that are part of this cycle.
4. Filter out any transactions from this cycle that have a `duration` strictly less than 60 seconds (i.e., keep transactions where `duration >= 60`).
5. Sort the remaining transactions primarily by `duration` in descending order. If two transactions have the same duration, sort them by `tx_id` in ascending order.
6. Paginate the sorted results to extract only the top 2 longest-running transactions in the cycle (i.e., page 1, where page size is 2).
7. Export this final list of transaction objects as a JSON array to a file named `/home/user/deadlock_report.json`.

You should run your Go program to generate the required output file before completing the task. 

Constraints:
- Do not install third-party Go graph libraries; implement the cycle detection using standard Go.
- Ensure the output file `/home/user/deadlock_report.json` contains exactly the JSON array of the top 2 filtered transaction objects.
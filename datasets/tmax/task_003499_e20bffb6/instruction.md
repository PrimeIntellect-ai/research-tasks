You are a data engineer tasked with building an ETL pipeline step to process distributed database logs. We are investigating transaction deadlocks. 

You have a dataset of transaction wait-logs located at `/home/user/etl_project/transactions.jsonl`. Each line is a JSON object representing a transaction waiting for another transaction to release a lock.

The schema of each line is:
- `tx_id` (string): The ID of the blocked transaction.
- `waits_for` (string): The ID of the transaction currently holding the lock.
- `wait_time_ms` (integer): How long `tx_id` has been waiting.

Your task is to write a Rust program within the existing Cargo project at `/home/user/etl_project` that performs the following processing:
1. **Graph Pattern Matching:** Parse the JSONL file and build a dependency graph to find all "deadlocks". A deadlock is defined as a cycle in the `waits_for` graph. (Note: A transaction will wait for at most one other transaction).
2. **Window/Analytical Aggregation:** For each detected cycle, calculate:
   - `total_wait_ms`: The sum of `wait_time_ms` for all edges in the cycle.
   - `max_wait_tx`: The `tx_id` of the transaction in the cycle that has the highest `wait_time_ms`.
3. **NoSQL Aggregation Pipeline:** Transform the results into a JSON array of objects, one for each deadlock cycle. 
4. **Ordering & Formatting:** 
   - Each object must have the keys: `cycle` (array of strings), `total_wait_ms` (integer), and `max_wait_tx` (string).
   - Sort the `cycle` array alphabetically.
   - Sort the final JSON array of cycles in descending order by `total_wait_ms`. If there is a tie, sort alphabetically by the first element of the sorted `cycle` array.
   - Save the output as a valid JSON file to `/home/user/etl_project/deadlock_report.json`.

You may use standard Cargo commands and modify the `src/main.rs` file. The project already has `serde` and `serde_json` dependencies configured. Once your Rust program is written, compile and run it to generate the report.
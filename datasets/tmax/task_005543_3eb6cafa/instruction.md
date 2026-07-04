You are acting as a Database Administrator optimizing queries and investigating system stalls. We have experienced a severe database freeze caused by a transaction deadlock. 

To prevent this from happening manually again, we need a tool to analyze lock states.

You have been provided with an export of the current lock requests in `/home/user/locks.csv`. The file has three columns: `tx_id`, `resource`, and `state`. 
- `tx_id`: The integer ID of the transaction.
- `resource`: The name of the database table being locked.
- `state`: Either `HOLDING` (the transaction currently holds an exclusive lock on the resource) or `WAITING` (the transaction is blocked, waiting to acquire a lock on the resource).

Your task is to:
1. Write a Rust program at `/home/user/detector.rs`.
2. The program must read `/home/user/locks.csv` and build a dependency graph. A dependency exists if Transaction A is `WAITING` for a resource that Transaction B is `HOLDING` (i.e., A depends on B).
3. Identify the deadlock by finding the cycle in this dependency graph. There is exactly one simple cycle representing the deadlock.
4. Output the `tx_id`s involved in the deadlock cycle, sorted in ascending numerical order, comma-separated, into a file named `/home/user/deadlock.txt` (e.g., `45,89,102`).
5. Compile your Rust program using standard `rustc` and run it to produce the output file.

Only output the `tx_id`s directly involved in the cycle itself. Do not include transactions that are waiting on the cycle but are not part of the closed loop.
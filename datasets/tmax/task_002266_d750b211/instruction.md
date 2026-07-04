You are acting as a technical assistant to a compliance officer auditing a suspected money laundering network. 

We have a scanned mandate at `/app/audit_policy.png`. Extract the constraints from this image (using OCR tools like `tesseract`) to find the **Minimum Transfer Amount** and the **Maximum Graph Traversal Depth** (hops).

We also have a SQLite database at `/app/financials.db` containing two tables:
1. `accounts` (id INTEGER PRIMARY KEY, type TEXT)
2. `transfers` (source INTEGER, target INTEGER, amount REAL)

**CRITICAL WARNING:** Our database engineers reported that the index `idx_transfers_source` on the `transfers` table was corrupted during a recent crash. If you run a standard `SELECT target FROM transfers WHERE source = ?`, SQLite will likely use the corrupted index and return stale/missing rows. You must bypass this index in your queries (e.g., using `NOT INDEXED` or by dropping it).

Your task is to write a C++ program that performs a graph traversal audit to find all reachable accounts. 

Create a C++ program at `/home/user/audit.cpp` and compile it to `/home/user/audit_cli` (use `-lsqlite3` and any other standard libraries you need, JSON libraries like `nlohmann-json3-dev` can be installed via apt).

The compiled program must accept exactly three integer arguments:
`/home/user/audit_cli <start_account_id> <offset> <limit>`

Your program must:
1. Hardcode the **Minimum Transfer Amount** and **Maximum Traversal Depth** constraints recovered from the image.
2. Connect to `/app/financials.db` and bypass the corrupted index.
3. Perform a Breadth-First Search (BFS) starting from `<start_account_id>` up to the Maximum Traversal Depth. 
4. Only traverse edges in `transfers` where `amount >= <Minimum Transfer Amount>`.
5. Collect the unique `id`s of all visited accounts (do NOT include the `start_account_id` itself in the final results).
6. Sort the collected IDs in strictly **descending** order.
7. Apply pagination using the `<offset>` and `<limit>` arguments.
8. Print the result to `stdout` in the following strict JSON schema and exit:
```json
{
  "total_reachable": 15,
  "paginated_results": [402, 350, 99]
}
```
If offset is greater than the total reachable nodes, `paginated_results` should be `[]`. Do not print anything else to `stdout`.

To succeed, your program must perfectly match the expected output format and logic across various randomly chosen inputs, matching our secure reference implementation.
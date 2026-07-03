You are a Database Administrator analyzing a sudden spike in concurrent transaction deadlocks. You have a SQLite database `/home/user/locks.db` containing a `lock_requests` table with historical data of transaction locks. 

Your goal is to extract lock dependency edges, model them as an RDF graph, and use a graph query to find all deadlocked transaction cycles.

The `lock_requests` table has the following schema:
- `tx_id` (TEXT): The transaction identifier.
- `resource_id` (TEXT): The identifier of the locked resource.
- `request_time` (INTEGER): The timestamp when the lock was requested.
- `grant_time` (INTEGER): The timestamp when the lock was granted (NULL if never granted due to deadlock).
- `release_time` (INTEGER): The timestamp when the lock was released (NULL if never released).

### Step 1: Extract "Wait-For" Dependencies
Write a Python script to query `/home/user/locks.db`. You must use a **SQL Window Function** to determine which transactions were waiting on which.
A transaction `TxA` is defined to "wait for" transaction `TxB` if:
1. They are requesting/holding locks on the same `resource_id`.
2. `TxB` was granted the lock (its `grant_time` is not NULL).
3. `TxA` requested the lock (`request_time`) *after* `TxB` was granted the lock, but *before* `TxB` released the lock (if `TxB`'s `release_time` is NULL, treat it as holding the lock indefinitely).
4. `TxB` is the *most recent* transaction to be granted the lock before `TxA`'s request. (This is where a window function like `LAG` or `LAST_VALUE` over a window partitioned by `resource_id` ordered by time is required).

### Step 2: Build an RDF Graph
Export these "Wait-For" edges into an RDF Turtle file at `/home/user/wait_for.ttl`.
Use the namespace `http://example.org/tx#`.
For every dependency where `TxA` waits for `TxB`, create an RDF triple that represents `TxA` waits for `TxB`. Use the predicate `http://example.org/tx#waitsFor`.
Example triple in Turtle:
`<http://example.org/tx#Tx1> <http://example.org/tx#waitsFor> <http://example.org/tx#Tx2> .`

### Step 3: Find Deadlocks using SPARQL
Write a Python script using the `rdflib` library to load `/home/user/wait_for.ttl` and execute a **SPARQL query** to find all deadlocked cycles.
A deadlock is defined as any closed cycle of `waitsFor` relationships of length 2 or 3 (e.g., A waits for B, B waits for A; OR A waits for B, B waits for C, C waits for A).

### Step 4: Export Results
Export the detected deadlocks as a JSON list of lists to `/home/user/deadlocks.json`.
- Each inner list represents a cycle of deadlocked `tx_id`s (e.g., `["Tx1", "Tx2"]`).
- Strip the URI prefix, leaving only the `tx_id` string (e.g., "Tx1").
- **Formatting Rules:**
  - Sort the `tx_id`s alphabetically within each cycle (e.g., `["Tx1", "Tx2"]` instead of `["Tx2", "Tx1"]`).
  - Sort the outer list of cycles alphabetically based on the first element of each inner list.
  - Remove duplicate cycles (a cycle `["Tx1", "Tx2"]` is the same as `["Tx2", "Tx1"]`).

Install any necessary Python libraries (like `rdflib`) using `pip`.
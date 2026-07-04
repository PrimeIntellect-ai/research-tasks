Hello! I am a researcher analyzing system logs to understand transaction deadlocks in our datasets. I've parsed our transaction logs into a SQLite database located at `/home/user/dataset.db`. 

The database has a single table representing transaction lock waits:
```sql
CREATE TABLE wait_graph (
    waiting_tx TEXT,
    blocking_tx TEXT
);
```
Each row indicates that `waiting_tx` is waiting on a lock currently held by `blocking_tx`. A deadlock occurs when there is a cycle in this graph (e.g., A waits for B, B waits for A).

I need you to write a Go program at `/home/user/find_deadlocks.go` that does the following:
1. Connects to the SQLite database.
2. Identifies all simple cycles (deadlocks) in the `wait_graph`. A cycle is a list of transactions where each waits on the next, and the last waits on the first.
3. Filters out duplicate cycles (e.g., A->B->A is the same as B->A->B). Represent each unique cycle starting with the transaction that comes first alphabetically.
4. Sorts the list of cycles alphabetically by their first element, then second element, etc.
5. Writes the result to `/home/user/deadlocks.json` strictly matching this JSON schema structure:
```json
{
  "deadlocks": [
    ["Tx1", "Tx2", "Tx3"],
    ["Tx4", "Tx5"]
  ]
}
```

You will need to initialize a Go module in `/home/user/` and use the `github.com/mattn/go-sqlite3` driver. 

Please write the code, run it, and ensure `/home/user/deadlocks.json` is created with the correct validation format.
You are a Database Reliability Engineer (DBRE) investigating a series of stalled backup jobs in a distributed database system. You suspect that concurrent backup transactions are deadlocking each other by acquiring and waiting on conflicting resource locks.

The lock manager exports its event logs in a JSONL (JSON Lines) format, acting as a NoSQL document stream. This log contains the state of all locks requested and acquired by various transactions. 

Your task is to write a Go program that processes this log stream, builds a Wait-For Graph (a type of knowledge graph mapping transaction dependencies), traverses the graph to detect deadlocks (cycles), and outputs a structured JSON report.

**Data Schema:**
The input file is located at `/home/user/transactions.jsonl`. Each line is a JSON object with the following fields:
- `tx_id` (string): The ID of the transaction (e.g., "TX1").
- `action` (string): Either `"ACQUIRED"` (the transaction successfully locked the resource) or `"WAITING"` (the transaction is blocked waiting for the resource).
- `resource` (string): The name of the resource (e.g., "TABLE_A_BACKUP").
- `timestamp` (integer): Epoch timestamp of the event.

**Wait-For Graph Logic:**
- A transaction `TxA` is WAITING for `TxB` if `TxA` has a `"WAITING"` event for a resource, and `TxB` has an `"ACQUIRED"` event for that *same* resource.
- A deadlock occurs if there is a cycle in the Wait-For Graph (e.g., TxA waits for TxB, TxB waits for TxC, TxC waits for TxA).

**Requirements:**
1. Write a Go program at `/home/user/detect.go`. You can use standard library packages only.
2. The program must parse `/home/user/transactions.jsonl`.
3. Construct the Wait-For Graph and traverse it to find *all* transaction IDs that are part of *any* deadlock cycle.
4. The program must output a strictly validated JSON file to `/home/user/deadlocks.json` containing exactly one object with the key `deadlocked_transactions`. The value must be a JSON array of strings containing the deadlocked transaction IDs, sorted alphabetically.

**Expected Output Schema for `/home/user/deadlocks.json`:**
```json
{
  "deadlocked_transactions": ["TX1", "TX2", "TX3"]
}
```

Run your Go program to generate the output file.
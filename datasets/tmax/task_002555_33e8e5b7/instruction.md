You are a backup administrator tasked with archiving database Write-Ahead Logs (WAL) and extracting their associated multi-line error logs to create a consolidated backup manifest. 

The database outputs data into two locations:
1. **WAL Files**: Scattered in subdirectories under `/home/user/db_data/`. 
2. **Server Logs**: A single log file at `/home/user/db_logs/server.log` containing multi-line records.

Your task is to write and execute a Go program at `/home/user/archive_wal.go` that performs the following steps:

1. **Recursive Traversal**: Traverse `/home/user/db_data/` to find all files ending with `.wal`.
2. **Binary Parsing**: Read the header of each `.wal` file. A valid WAL file starts with a 4-byte magic signature `WAL\x01`, immediately followed by a 4-byte unsigned little-endian integer representing the `TransactionID` (tx_id). Ignore any `.wal` files that do not have this exact 4-byte magic signature.
3. **Multi-line Log Parsing**: For each valid WAL file, find its corresponding log entry in `/home/user/db_logs/server.log`. 
   - Log entries begin with a header line strictly formatted as `[TX: <TransactionID>]` (e.g., `[TX: 1042]`).
   - The log snippet for this transaction includes all subsequent lines up to (but excluding) the next `[TX: ...]` header or the end of the file. Strip leading/trailing whitespace from the extracted snippet.
4. **Atomic JSON Export**: Consolidate the extracted information into a JSON array of objects, sorted by `tx_id` in ascending order. Write this JSON array to a temporary file first, and then atomically rename it to `/home/user/backup_manifest.json`.

The final `/home/user/backup_manifest.json` must exactly match this structure:
```json
[
  {
    "file": "/home/user/db_data/partition1/001.wal",
    "tx_id": 1042,
    "log_snippet": "Error: Checkpoint timeout\nRetrying flush..."
  },
  ...
]
```

Write the Go program, run it, and ensure `/home/user/backup_manifest.json` is successfully created with the correct data.
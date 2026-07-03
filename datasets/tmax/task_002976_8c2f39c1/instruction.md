You are a data analyst investigating database concurrency issues. You have been provided with a CSV file containing lock wait events, representing which database transactions are waiting for locks held by other transactions.

Your task is to write a Bash script that processes this CSV file, identifies deadlocks using a recursive query, and exports the findings into a specific JSON format. 

Here are the details:
1. The input file is located at `/home/user/waits.csv`. It has a header row and three columns: `waiting_trx`, `blocking_trx`, and `resource`.
   - `waiting_trx`: The ID of the transaction that is blocked.
   - `blocking_trx`: The ID of the transaction holding the lock.
   - `resource`: The database resource being contested.
2. Create a Bash script at `/home/user/detect_deadlocks.sh`. When executed, this script should:
   - Create a temporary SQLite database.
   - Import the `waits.csv` data into a table named `lock_waits`.
   - Execute a Recursive Common Table Expression (CTE) query to find all transaction IDs that are part of a deadlock cycle (e.g., A waits for B, and B waits for A; or A waits for B, B waits for C, and C waits for A).
   - Export a distinct list of these deadlocked transaction IDs as a JSON array of strings, sorted alphabetically.
   - Save the final JSON output to `/home/user/deadlocks.json`.

**Expected Output Format:**
The file `/home/user/deadlocks.json` should look exactly like this:
```json
[
  "TRX_A",
  "TRX_B",
  "TRX_C"
]
```

Make sure your script is executable (`chmod +x /home/user/detect_deadlocks.sh`) and runs successfully without user intervention.
You are a performance engineer tasked with post-mortem analysis and profiling of a recently crashed microservices environment. The system crashed due to a misconfiguration, leaving behind fragmented logs, an uncommitted database Write-Ahead Log (WAL), and an endpoint suffering from unknown performance bottlenecks.

Your objectives are to reconstruct the event timeline, recover lost data, and profile the application to find the performance bottleneck.

**Phase 1: Log Timeline Reconstruction**
The application components log to three different files in `/home/user/logs/`. Each uses a slightly different timestamp format:
1. `/home/user/logs/web.log` - Format: `[YYYY-MM-DD HH:MM:SS] LEVEL Message`
2. `/home/user/logs/worker.log` - Format: `HH:MM:SS YYYY-MM-DD | LEVEL | Message`
3. `/home/user/logs/db.log` - Format: `YYYY/MM/DD-HH:MM:SS - LEVEL - Message`

Write a script in the language of your choice to parse, normalize, and merge these logs chronologically. Identify the exact timestamp of the `FATAL` log entry that caused the crash.

**Phase 2: Database Recovery from WAL**
The crash interrupted a critical transaction. In `/home/user/app/`, you will find `data.db` (SQLite3) and its uncommitted `data.db-wal` file. 
Recover the database by forcing a checkpoint or reading the WAL, and extract the `secret_token` from the `transactions` table. The latest transaction is currently only present in the WAL.

**Phase 3: Performance Profiling via Fuzzing**
There is a standalone mock application at `/home/user/app/server.py`. It accepts a single string argument (e.g., `python3 /home/user/app/server.py "test_input"`). Under normal conditions, it executes in a few milliseconds. However, specific input patterns cause severe latency spikes (> 500ms).
Write a fuzz testing script to generate random alphanumeric inputs and test the script. Discover the specific 6-character uppercase substring that triggers the performance bottleneck. 

**Verification Requirement:**
Create a JSON file at `/home/user/report.json` with the following exact structure:
```json
{
  "crash_timestamp": "YYYY-MM-DD HH:MM:SS",
  "recovered_token": "TOKEN_VALUE",
  "bottleneck_substring": "XXXXXX"
}
```
Ensure all extracted values are highly accurate. You may write any auxiliary scripts in the language of your choice to complete these tasks.
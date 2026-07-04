You are an operations engineer triaging an incident. A critical Python-based event processing system crashed overnight. The system was heavily multithreaded and wrote to a custom Write-Ahead Log (WAL) before committing to the main database. 

It appears the system experienced a deadlock under high contention, causing a severe processing delay (an anomaly) right before the watchdog forcefully killed the process, leaving the WAL file corrupted.

You have been provided an archive of the system state right after the crash in `/home/user/incident_data`. 

The directory contains:
1. `service.log`: A merged log containing interleaved entries from multiple threads. Format: `[TIMESTAMP] [THREAD_ID] [LEVEL] Message`.
2. `transactions.wal`: A text-based Write-Ahead Log. Each valid entry is on a single line with the format: `TXN_ID:START_TIMESTAMP:END_TIMESTAMP:PAYLOAD_HASH`. The file was truncated when the process was killed.

Your task is to analyze these files and generate an incident report. You will likely need to write a short Python script to process the data.

Please determine the following:
1. **Deadlocked Threads**: Identify the two `THREAD_ID`s involved in the deadlock. A deadlock occurred because Thread A acquired a resource and was waiting for a resource held by Thread B, while Thread B was waiting for a resource held by Thread A.
2. **Anomalous Transaction**: Based on the valid entries in the `transactions.wal`, calculate the duration (END_TIMESTAMP - START_TIMESTAMP) of each transaction. Identify the `TXN_ID` of the transaction that took exceptionally longer than the rest (a statistical anomaly, at least 10x the median duration).
3. **Last Recoverable Transaction**: Identify the highest `TXN_ID` that is completely and validly written to the `transactions.wal`. A valid entry must have exactly 4 colon-separated fields, and `PAYLOAD_HASH` must be exactly 8 alphanumeric characters. The last line might be partially written or missing fields.

Output your findings by creating a JSON file strictly at `/home/user/incident_report.json` with the following exact keys and types:
- `"deadlock_thread_1"`: (string) The ID of one deadlocked thread (e.g., "Thread-X"). Order does not matter between 1 and 2.
- `"deadlock_thread_2"`: (string) The ID of the second deadlocked thread.
- `"anomalous_txn_id"`: (string) The ID of the slow transaction (e.g., "TXN-Y").
- `"last_recovered_txn_id"`: (string) The ID of the last intact transaction in the WAL.
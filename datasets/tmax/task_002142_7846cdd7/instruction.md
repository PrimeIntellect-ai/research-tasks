You are a reliable backend engineer investigating a sudden Out-Of-Memory (OOM) crash in a long-running Python transaction processing service. The service crashed recently due to a massive memory leak triggered by a concurrency bug.

You have been provided with the following directories and files:
1. `/home/user/logs/api.log`: Logs of incoming API requests.
2. `/home/user/logs/worker.log`: Thread-level logs of the Python workers processing the transactions.
3. `/home/user/logs/db.log`: Logs of the database writer committing transactions.
4. `/home/user/wal/`: A directory containing Write-Ahead Log (WAL) files (`wal_001.dat` to `wal_050.dat`) created by the database writer.

Your task:
1. Reconstruct the timeline of events right before the crash. The system experienced a race condition where the exact same Transaction ID (TXN) was mistakenly assigned to *two* different worker threads simultaneously, causing an infinite loop of memory allocation that led to the OOM.
2. Identify the culprit Transaction ID.
3. Locate the specific corrupted WAL file in `/home/user/wal/` that corresponds to this Transaction ID. The corrupted file will contain the string `STATUS:UNCOMMITTED` alongside the culprit TXN ID.

Once you have deduced the transaction ID and the exact absolute path to the corrupted WAL file, create a report file at `/home/user/report.txt` with exactly the following format:
```
TXN_ID: <Culprit-Transaction-ID>
WAL_FILE: <Absolute-Path-To-Corrupted-WAL>
```
For example:
```
TXN_ID: TXN-1234
WAL_FILE: /home/user/wal/wal_005.dat
```
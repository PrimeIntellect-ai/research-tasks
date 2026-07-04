You are a DevOps engineer debugging a log ingestion script. 

We have a Python script located at `/home/user/log_merger.py` that reads binary log files from multiple services, parses them, and reconstructs a unified chronological timeline of events. The script uses multiprocessing to parse files concurrently and sends the parsed records to a shared queue.

However, the system recently started hanging indefinitely and failing to produce the output. 

Here is what we know:
1. The binary logs are stored in `/home/user/logs/service_A/` and `/home/user/logs/service_B/`. Each record is exactly 8 bytes long (4 bytes for a timestamp, 4 bytes for a value, both little-endian).
2. The legacy systems generating these logs sometimes suffer from signed integer overflow, producing corrupted records that unpack to negative timestamps. 
3. The script contains an assertion (`assert ts >= 0`) as an intermediate validation step to catch these overflows.
4. When this assertion trips, a worker process crashes. Because of how the concurrency is implemented, this causes a deadlock (a classic race condition where the main process waits forever for a sentinel value that never arrives).

Your task is to fix the script `/home/user/log_merger.py` so that:
- It safely handles corrupted inputs: any record with a negative timestamp should simply be skipped.
- It prevents concurrency deadlocks: ensure that worker processes always signal completion to the main process, even if they encounter unexpected exceptions or assertions.
- It successfully outputs the complete, sorted timeline to `/home/user/merged_timeline.json`.

Do not change the output file path or the JSON schema. Once you have fixed the script, run it so that `/home/user/merged_timeline.json` is generated.
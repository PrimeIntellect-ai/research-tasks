You are a support engineer investigating a severe issue in our distributed telemetry ingestion pipeline. Customers are reporting that some telemetry events are mysteriously dropped, while others are processed with negative durations. 

The system consists of three services located in `/home/user/app/`:
1. **Flask API** (`api.py`): Ingests JSON telemetry events.
2. **Redis**: Acts as a message broker.
3. **Worker** (`worker.py`): Consumes events from Redis, calculates duration based on timestamps, and writes successful processing logs.

When you run `/home/user/app/start_services.sh`, the services fail to communicate, and the pipeline remains broken.

Your tasks are as follows:

**Phase 1: Multi-Service Composition & Debugging**
1. Inspect and fix the configuration files and environment variables so that the Flask API correctly communicates with Redis, and the Worker correctly pulls from the same Redis instance. 
2. Use interactive debugging and log analysis to diagnose a timezone handling bug between `api.py` and `worker.py`. The API receives ISO-8601 strings (e.g., "2023-10-15T14:30:00Z"), but subtle naive vs. timezone-aware datetime mismatches are causing race conditions and negative duration calculations in the worker. Fix the code in `/home/user/app/api.py` and `/home/user/app/worker.py` so that events are accurately processed and logged.

**Phase 2: Forensic Log Detector**
Due to the timezone bug, we have months of corrupted historical logs mixed with valid ones. You must write a forensics detector script at `/home/user/detector.py`.
The script must take a single file path as a command-line argument:
`python3 /home/user/detector.py <path_to_log_file.jsonl>`

The script must analyze the JSONL log file and determine if it contains ANY entries affected by the timezone corruption (e.g., implied negative durations or out-of-order timestamp processing caused by the UTC offset bug). 
- If the log file is entirely clean, the script must exit with status code `0`.
- If the log file contains ANY corrupted "evil" entries, the script must exit with status code `1`.

Your detector will be tested against two internal corpora (one consisting entirely of clean logs, and another of corrupted logs). It must be 100% accurate.
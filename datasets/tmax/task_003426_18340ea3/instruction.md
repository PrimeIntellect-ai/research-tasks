You are a performance engineer tasked with profiling and debugging a local distributed file processing application. The application processes text files concurrently using a bash script that spawns Python worker clients, which in turn send data to a Python server. 

Recently, the system has been failing to process all files, and sometimes the server hangs indefinitely. 

You have been provided with the following files in `/home/user/app/`:
1. `runner.sh`: A shell script intended to loop over all files in `/home/user/app/data/` and pass them to the worker client.
2. `server.py`: A Python server that listens for incoming file processing requests.
3. `worker.py`: A Python client that reads a file and sends its contents to the server.
4. `capture.pcap`: A network packet capture of the loopback interface during a recent hung session.

Your objectives:

**Phase 1: Shell Script Debugging**
`runner.sh` is failing to process files with spaces in their names, causing the script to pass fragmented filenames to the Python worker, which leads to `FileNotFoundError`s and missing data. Fix `runner.sh` so that it correctly passes the exact, full filename (including spaces) to `worker.py`.

**Phase 2: Network & Concurrency Analysis**
The server occasionally hangs. Use `tcpdump` or Python tools to analyze `capture.pcap`. You will notice the communication stops abruptly. Look into `server.py`. There is a concurrency bug (a race condition/deadlock) when updating the shared processing statistics. 
Diagnose and fix the concurrency bug in `server.py` so that it correctly handles concurrent client requests without deadlocking or leaking locks, even if the payload triggers an error branch.

**Phase 3: Minimal Reproducible Example**
Create a Python script at `/home/user/app/mre.py` that programmatically demonstrates the Python concurrency bug is fixed. This script must:
1. Start the `server.py` in a background thread or process.
2. Simultaneously spawn 5 threads that each send the payload `"ERROR_TRIGGER"` to the server (which previously caused the server to hang).
3. Successfully exit with code 0 within 5 seconds, proving the server successfully responded to or closed all connections without deadlocking.

**Phase 4: Reporting**
Generate a JSON report at `/home/user/app/report.json` with the following schema:
```json
{
  "pcap_final_dst_port": <int, the destination port of the final TCP packet in capture.pcap>,
  "deadlock_cause": "<string, brief explanation of why server.py hung>"
}
```

Ensure all your fixes are applied directly to the files in `/home/user/app/`. The automated test will verify your fixes by running `runner.sh` and `mre.py`, and evaluating `report.json`.
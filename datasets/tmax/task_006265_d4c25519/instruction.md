You are a DevOps engineer tasked with resolving a critical pipeline failure. 

Our log aggregation pipeline is suddenly crashing with a Segmentation Fault. The pipeline consists of a Bash script `process.sh` that feeds log files into a compiled C program called `log_parser`.

You have been provided with:
1. A Git repository at `/home/user/log_pipeline` containing the source code (`log_parser.c` and `process.sh`).
2. A directory of distributed raw logs at `/home/user/raw_logs/`.

Your objective is to debug this issue by performing the following steps:
1. **Regression Finding:** The main branch `HEAD` is crashing on the provided logs, but an older commit is known to work. Use Git bisection to find the exact commit that introduced the segmentation fault.
2. **Crash Analysis:** Compile the buggy version of `log_parser.c` with debug symbols. Run it using `gdb` (or generate a core dump) to analyze the crash. Identify the exact malicious/oversized string payload that is causing the buffer overflow.
3. **Log Timeline Reconstruction:** Search across the distributed log files in `/home/user/raw_logs/` to trace back where this malicious payload originated. Identify the service name (the filename without the `.log` extension) and the exact timestamp when this payload was received.

Once you have gathered this information, create a JSON report at `/home/user/incident_report.json` with the following precise structure:

```json
{
  "bad_commit_message": "The exact commit message of the commit that introduced the bug",
  "crashing_payload": "The exact string payload extracted from the crash analysis (just the value, e.g., 'ABCDEFG...')",
  "originating_service": "service_name",
  "timestamp": "YYYY-MM-DDThh:mm:ssZ"
}
```

Notes:
- The git repository contains a script `build.sh` to compile the C program.
- The `process.sh` script takes a directory of logs as an argument, e.g., `./process.sh /home/user/raw_logs/`.
- Ensure your final JSON file is strictly valid.
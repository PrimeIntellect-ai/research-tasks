You are an operations engineer triaging an incident with our legacy analytics pipeline. The main reporting script, located at `/home/user/analytics_repo/process.py`, has suddenly started failing and, when it does run, produces mathematically incorrect reports.

The pipeline consists of a local Git repository in `/home/user/analytics_repo/`. You need to investigate and fix the pipeline to generate the correct daily report. 

Perform the following debugging phases:

**Phase 1: Secret Recovery (Git Forensics)**
The script requires a secret key to decrypt the data payload. A previous developer accidentally committed this 32-character hex key into the Git repository's history in a file called `secrets.json`, but later deleted it. 
1. Find the deleted 32-character hex key in the Git history.
2. Save this exact key to a file at `/home/user/key.txt`.

**Phase 2: System Call Tracing**
Even with the correct key, the script currently exits silently with status code 1. No logs are produced.
1. Trace the script's execution to determine what missing resource is causing the crash.
2. You will find it is trying to read a specific hidden file in `/home/user/`. Create this missing file and populate it with the exact string `TOKEN_OK`.

**Phase 3: Floating-Point Precision Repair**
Once the script runs, it will process `/home/user/analytics_repo/transactions.csv` and write the output to `/home/user/total.txt`. 
If you inspect the output, you will notice standard floating-point accumulation errors (e.g., producing values like `Total: 1005.6000000000001` instead of `Total: 1005.60`).
1. Modify `/home/user/analytics_repo/process.py`.
2. Fix the precision bug in the calculation logic. You must use Python's `decimal` module to accurately sum the currency values. 
3. Run the fixed script. The final output in `/home/user/total.txt` must be strictly formatted as `Total: <amount>`, with exactly two decimal places (e.g., `Total: 1005.60`).

Ensure all tasks are complete, the script is fully functional, and `/home/user/total.txt` contains the correct, precision-fixed sum before finishing.
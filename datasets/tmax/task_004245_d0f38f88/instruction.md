You are an on-call engineer who just got paged at 3 AM. The "MathEngine" microservice has been crashing repeatedly, causing upstream timeouts. 

You need to investigate and fix the system. Here is what you know:

1. **Log Timeline Reconstruction**: There are two log files located at `/home/user/logs/frontend.log` and `/home/user/logs/backend.log`. The frontend logs timeouts/connection drops, and the backend logs the start of processing and fatal errors. Correlate the logs to identify the exact Request IDs of the requests that caused the backend to crash. Write these Request IDs (one per line) to `/home/user/crashing_ids.txt`.

2. **Corrupted Input Handling**: The backend script at `/home/user/app/backend.py` processes a data file `/home/user/data/payload.jsonl`. Some of the inputs are corrupted (e.g., malformed matrices, non-square matrices, or invalid data types), which is causing the script to crash instead of gracefully skipping them. 
Modify `/home/user/app/backend.py` so that it catches these errors, skips the invalid entries, and continues processing.

3. **Dependency Conflict & Execution**: The script currently relies on a `requirements.txt` file in `/home/user/app/`. However, the environment isn't set up correctly. Create a virtual environment at `/home/user/venv`, install the necessary dependencies (resolving any missing package issues), and run the fixed `/home/user/app/backend.py`. 

The modified `backend.py` must calculate the sum of the determinants of all *valid* matrices in the payload and write this total sum (as a float) to `/home/user/result.txt`. 

Verify that your `/home/user/crashing_ids.txt` contains exactly the IDs of the crashed requests, and `/home/user/result.txt` contains the sum of the determinants of the valid matrices.
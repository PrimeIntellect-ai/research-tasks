You are an operations engineer triaging a critical incident. A custom Python-based logging service crashed under suspicious circumstances. 

The service's main database file was completely corrupted, but the Write-Ahead Log (WAL) survived. We have a recovery script, but it's failing to extract all the records. Forensic analysis indicates the final record in the WAL contains the IP address of the attacker who triggered the crash, but the recovery script is currently missing it due to a boundary condition/off-by-one bug in the parsing logic.

Your tasks:
1. Navigate to `/home/user/incident/`.
2. Analyze `recover.py` and `db.wal`. Use an interactive debugger (like `pdb`) or logging to understand the custom binary format and find the parsing bug.
3. Fix the off-by-one/boundary error in `recover.py` so that it successfully parses the entire `db.wal` file without skipping the final record or throwing an error.
4. Run the fixed `recover.py`. It is hardcoded to read `db.wal` and output the recovered records to `/home/user/incident/recovered_db.json`.
5. Parse `/home/user/incident/recovered_db.json` to find the `"source_ip"` associated with the event where `"action": "SYSTEM_CRASH"`.
6. Write ONLY that IP address to `/home/user/attacker_ip.txt`.

Ensure your fix correctly handles the binary offsets and lengths as defined in the file format. Do not just manually write the IP address; you must fix the recovery script to produce the full valid JSON array.
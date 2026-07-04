You are acting as an automated technical assistant for a compliance officer. The officer is auditing a financial system to detect "circular funding" schemes—a form of money laundering where funds move in a closed loop. 

You have been provided with a raw transaction dataset at `/home/user/compliance_audit/tx_data.csv`. The file has the following header: `tx_id,sender_id,receiver_id,amount,timestamp`.

Your task is to build a data querying pipeline in Python to detect these circular funding loops.

Perform the following steps:

1. **Database Ingestion & Indexing (`/home/user/compliance_audit/ingest.py`)**:
   Write a Python script that reads `tx_data.csv` and loads it into an SQLite database at `/home/user/compliance_audit/audit.db`. The table should be named `transactions`.
   Crucially, you must design and execute an indexing strategy on this table. Without proper indexes, the graph traversal queries in the next step will take far too long to execute.

2. **Cycle Detection Pipeline (`/home/user/compliance_audit/detect_cycles.py`)**:
   Write a Python script that accepts a single command-line argument: `min_amount`. 
   The script must connect to `audit.db` and use a complex SQL join to find all cycles of length exactly 3 (A -> B -> C -> A).
   Constraints for a valid cycle:
   - Each transaction in the cycle must have an `amount` strictly greater than `min_amount`.
   - You must use parameterized query construction (do not use string formatting/f-strings for the `min_amount` value in your SQL query).
   - Order the nodes in each cycle lexicographically so that `node1` < `node2` < `node3` when determining uniqueness, to avoid reporting the same cycle multiple times (e.g., A-B-C is the same as B-C-A).

3. **Output Generation (`/home/user/compliance_audit/report.json`)**:
   The `detect_cycles.py` script must output the findings to `/home/user/compliance_audit/report.json`.
   The output must strictly validate against this schema structure:
   ```json
   {
     "audit_threshold": <float>,
     "cycles_detected": [
       {
         "node1": "<string>",
         "node2": "<string>",
         "node3": "<string>",
         "bottleneck_amount": <float> 
       }
     ]
   }
   ```
   *Note: `bottleneck_amount` is the minimum `amount` among the 3 transactions making up that specific cycle.*
   The `cycles_detected` array should be sorted by `bottleneck_amount` descending, then by `node1` ascending.

Run your script with a threshold of `50000.0` like so:
`python3 /home/user/compliance_audit/detect_cycles.py 50000.0`

Ensure the final `report.json` is generated correctly.
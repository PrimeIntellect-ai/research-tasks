**Ticket #9942: Data Ingestion Pipeline Failure**

Hello IT Support,

Our nightly data ingestion script, located at `/home/user/processor.py`, is crashing when trying to process last night's batch of transactions located at `/home/user/data/input.jsonl`. 

The pipeline parses JSON Lines, decodes a serialized base64 payload within each transaction, batches the records, and inserts them into an SQLite database (`/home/user/transactions.db`). 

There are three issues you need to resolve:
1. **Crash during processing (Serialization Error):** The script crashes with a decoding error on a specific transaction. A rogue system upstream sometimes strips the base64 padding (`=`) from the `payload` field. You need to identify which transaction is causing this crash and update the `decode_payload` function in `processor.py` to automatically fix missing base64 padding before decoding.
2. **Missing Data (Boundary Condition):** The Accounting team audited previous successful runs and reported that exactly 1 transaction is mysteriously dropped from every 100-item batch! Please find and fix the off-by-one boundary bug in the `batch_records` function.
3. **Tracking:** We need to know exactly which transaction caused the pipeline to crash tonight. 

**Your Tasks:**
1. Fix the bugs in `/home/user/processor.py`.
2. Run the script so it successfully processes all records into `/home/user/transactions.db`.
3. Create a file named `/home/user/crash_id.txt` containing *only* the string ID (e.g., `TXN-123`) of the single transaction that had the malformed/unpadded base64 payload.
4. Create a file named `/home/user/total_processed.txt` containing *only* the integer representing the total number of records successfully inserted into the database after your fixes.

Please get this done as soon as possible.
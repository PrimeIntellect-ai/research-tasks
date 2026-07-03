You are an engineer investigating a long-running data service that recently crashed due to an Out-Of-Memory (OOM) error. 

Here is the current state of your system:
- The service was running a compiled executable located at `/app/leaky_processor`. This binary is now stripped of debug symbols.
- At the time of the crash, the service was reading from a SQLite database. The database files were left in a dirty/corrupted state at `/home/user/data/events.db` (along with its `-wal` and `-shm` files).
- The binary accepts two arguments: the path to the SQLite database, and the output JSON file path. Usage: `/app/leaky_processor <input.db> <output.json>`.

Your objectives:
1. **Database Recovery:** Recover the corrupted database into a clean SQLite database file at `/home/user/data/recovered.db`. 
2. **Behavior Analysis & Fuzzing:** The `/app/leaky_processor` binary reads the `records` table (which has `id` and `payload` columns). It applies a data transformation to the `payload` and writes a key-value mapping of `{id: transformed_payload}` to the output JSON. However, it contains a severe memory leak when processing certain malformed payloads (which act as accidental fuzz inputs).
3. **Re-implementation:** Write a safe, Python-based replacement script at `/home/user/safe_processor.py`. 
   - It must take two command-line arguments: `python3 /home/user/safe_processor.py <input.db> <output.json>`.
   - It must replicate the exact data transformation logic of the original binary for valid data.
   - It must use assertion-based validation to detect and skip/drop malformed payloads (preventing processing errors).
   - It must run with a stable, low memory footprint (no memory leaks).

Once you have created `/home/user/safe_processor.py`, our automated testing suite will evaluate it against a held-out database with millions of rows. It will be evaluated based on the functional accuracy of the output JSON and the peak memory consumption (RSS) during execution.
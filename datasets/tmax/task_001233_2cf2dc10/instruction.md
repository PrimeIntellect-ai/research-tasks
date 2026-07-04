You are a performance engineer tasked with debugging a profile aggregation pipeline located in `/home/user/profiler`.

Currently, the system is in a broken state due to a recent crash and some existing bugs in the aggregation script. Your goal is to recover the database, fix the script, add intermediate state tracing, and generate the final report.

Here are your tasks:

1. **Database Recovery**: 
   The SQLite database `/home/user/profiler/logs.db` was left in Write-Ahead Log (WAL) mode and the system crashed before it could checkpoint. A legacy downstream tool requires the database to be a single file without a `-wal` file. 
   - Checkpoint the WAL and change the database's journal mode to `DELETE` so that the `-wal` file is permanently removed and all data is safely in `logs.db`.

2. **Concurrency and Overflow Debugging**:
   The script `/home/user/profiler/process.py` reads the database and aggregates metrics using Python's `multiprocessing`. However, it has a couple of critical bugs:
   - **Integer Overflow**: The script uses a 32-bit signed integer (`'i'`) for a shared counter, which crashes with an `OverflowError` because the aggregated metrics exceed 2.14 billion. Change it to a 64-bit signed integer (`'q'`).
   - **Race Condition**: The shared values `total_metric` and `processed_count` are updated concurrently by multiple processes using `+=`. This operation is not atomic, leading to lost updates. Fix this race condition using the appropriate locking mechanism provided by the `multiprocessing` module.

3. **Intermediate State Tracing**:
   We need to trace the processing state. Modify `process.py` so that inside `process_chunk`, whenever a row's `id` is perfectly divisible by 100 (e.g., 100, 200, 300...), the script appends that `id` to `/home/user/profiler/trace.log` (one ID per line). Opening the file in append mode (`'a'`) inside the condition is sufficient.

4. **Execution**:
   Run the fixed `process.py`. It should successfully complete and write the correct totals to `/home/user/profiler/summary.json`.

**Acceptance Criteria**:
- `logs.db-wal` must not exist, and `logs.db` must have `journal_mode=delete`.
- `summary.json` must contain the exact correct `total_records` and `total_metric`.
- `trace.log` must contain the correct traced IDs.
- `process.py` must use safe locking for shared variables.
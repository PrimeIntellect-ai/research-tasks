You have inherited an unfamiliar legacy codebase located in `/home/user/legacy_app/`. The system processes data items from a SQLite database using a combination of a Bash orchestrator (`runner.sh`) and a compiled C binary (`bin/processor`). 

Recently, the system has started experiencing deadlocks under high contention. When `runner.sh` is executed, it spawns multiple background jobs that hang indefinitely. 

Your task is to debug and fix the pipeline:
1. **Memory Dump Analysis**: A previous process hung and dumped its memory to `/home/user/legacy_app/core_dumps/core.9999`. Extract the critical transaction ID that the process was handling when it hung. The ID is prefixed with `CRITICAL_TX_HANG: `. Write the extracted transaction ID (just the ID itself, e.g., `TX-12345`) to `/home/user/crash_tx.txt`.
2. **Binary Reverse Engineering & Bash Debugging**: Inspect the compiled `bin/processor` binary to find a hidden environment variable used by the original developers to bypass the legacy locking mechanism. Modify `/home/user/legacy_app/runner.sh` to correctly export this environment variable so that the deadlock no longer occurs.
3. **Execution & Query Debugging**: Run your fixed `runner.sh`. It should now complete successfully and populate `/home/user/legacy_app/results.db`. Query `results.db` to calculate the total sum of the `value` column in the `completed` table. Write this numeric sum to `/home/user/total_value.txt`.

Ensure your modifications to `runner.sh` are correct and all required output files are exactly as specified.
You are a Database Reliability Engineer investigating a recurring issue where automated backup jobs are causing application transactions to freeze. You suspect a deadlock is occurring between the backup processes and standard application queries.

You have exported the current lock state of the database into an SQLite database located at `/home/user/db_state.sqlite`. 

The database contains two tables:
1. `transactions`
   - `tx_id` (TEXT): The transaction identifier.
   - `type` (TEXT): The type of transaction ('backup' or 'app').
2. `locks`
   - `tx_id` (TEXT): The transaction requesting or holding the lock.
   - `resource_id` (TEXT): The ID of the locked resource (e.g., table or row).
   - `granted` (INTEGER): `1` if the transaction holds the lock, `0` if it is waiting for the lock.

Your task is to write a Bash script at `/home/user/analyze_locks.sh` that:
1. Uses `sqlite3` to query `/home/user/db_state.sqlite`.
2. Projects the lock data into a "wait-for" graph. A transaction A "waits for" transaction B if A has requested a lock on a resource (`granted = 0`) that is currently held by B (`granted = 1`).
3. Uses graph traversal (e.g., a Recursive CTE) to find a deadlock cycle. A deadlock cycle is a path in the wait-for graph where a transaction eventually waits for itself.
4. Identifies all `tx_id`s involved in the *shortest* deadlock cycle.
5. Writes the involved `tx_id`s to `/home/user/deadlock_result.txt`. The IDs must be sorted alphabetically and separated by a single comma (no spaces), e.g., `TX1,TX2,TX3`.

Ensure your script is executable and runs successfully without any manual arguments. Do not hardcode the expected answer; the database content may change in automated tests.
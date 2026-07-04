You are an on-call engineer responding to a 3 AM page. The backend background worker that processes incoming telemetry events has crashed violently, leaving the processing queue in an inconsistent state. The crash was triggered by a subtle timezone serialization bug that corrupted the memory and local data stores. 

Your objective is to investigate the crash, recover the lost data, and reconstruct the corrupted payload. 

Here is what you need to do:

1. **Git Forensics & Secret Recovery**: 
   The payload was encrypted using a legacy XOR cipher. The `SECRET_KEY` was accidentally committed to the worker's git repository located at `/home/user/worker_repo` a few commits ago, but was subsequently removed. Search the git history of this repository to find the string assigned to `SECRET_KEY`.

2. **Memory Dump Analysis**: 
   When the worker crashed, it dumped a raw memory segment to `/home/user/worker_dump.bin`. Inspect this binary file and extract the JSON string labeled `CRASH_CONTEXT`. Identify the value of the `last_event_id` from this context.

3. **Corrupted Input Handling & Encoding Troubleshooting**: 
   The event payload that caused the crash is stored at `/home/user/corrupt_payload.enc`. 
   - Decrypt the file by applying a repeating-key XOR operation using the `SECRET_KEY` you found in step 1.
   - The decrypted payload is a JSON string, but the `timestamp` field contains corrupted bytes due to an invalid timezone encoding (mixing UTF-8 and ISO-8859-1).
   - Fix the decoded string by replacing any invalid/non-ASCII characters in the timestamp with the literal string `+00:00`. The resulting string should be valid JSON. Extract the repaired `timestamp` value.

4. **Database Recovery**: 
   The crash left the local SQLite database at `/home/user/data/events.db` corrupted (the main file header was zeroed out). However, the Write-Ahead Log (`events.db-wal`) is still intact. Recover the data from the WAL into a readable format and determine the total number of rows in the `processed_events` table.

Once you have gathered all this information, create a JSON file at `/home/user/resolution.json` with the following exact structure:

```json
{
  "secret_key": "<recovered_secret_key_from_git>",
  "last_event_id": "<event_id_from_memory_dump>",
  "repaired_timestamp": "<the_fixed_timestamp_from_payload>",
  "recovered_db_row_count": <integer_count_of_rows>
}
```
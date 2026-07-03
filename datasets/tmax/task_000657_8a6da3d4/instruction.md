You are a DevOps engineer troubleshooting a failing data ingestion pipeline.

The pipeline code is located in `/home/user/app/`. It consists of a Python script `main.py` that reads records from `inputs.txt`, parses them using a custom C extension `fast_parser`, and inserts them into an SQLite database `data.db`.

Currently, the pipeline is broken in multiple ways:
1. The C extension fails to build due to a misconfiguration in the environment or build script.
2. Even when built, the script intermittently crashes with a Segmentation Fault due to a bug in the C extension when processing a specific input.
3. A previous crash has left the SQLite database `data.db` corrupted.

Your task:
1. Fix the build issue and compile the `fast_parser` extension in `/home/user/app/`.
2. Identify the exact string in `/home/user/app/inputs.txt` that triggers the Segmentation Fault (buffer overflow).
3. Recover the corrupted SQLite database `/home/user/app/data.db` using the `sqlite3` CLI tool (e.g., using the `.recover` or `.dump` command) and save the clean database to `/home/user/app/recovered.db`.
4. Create a JSON summary file at `/home/user/summary.json` with the following structure:
```json
{
  "crashing_input": "THE_EXACT_STRING_FROM_INPUTS_TXT_THAT_CRASHES",
  "recovered_records": 123
}
```
Replace `THE_EXACT_STRING_FROM_INPUTS_TXT_THAT_CRASHES` with the actual line from `inputs.txt` that causes the crash, and `123` with the integer number of rows recovered in the `events` table of `recovered.db`.

Constraints:
- You must write your findings exactly in the format specified in `/home/user/summary.json`.
- Do not modify the original `inputs.txt`.
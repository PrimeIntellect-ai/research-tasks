You are an operations engineer triaging an incident with a legacy data ingestion script. The script `/home/user/process.py` processes a JSONL file `/home/user/data.jsonl` and counts the number of valid records (records that contain a `value` key). It outputs the final count to `/home/user/output.txt`.

Currently, the pipeline is failing for three reasons:
1. **Dependency Conflict**: The script relies on a legacy `pandas` method (`DataFrame.append`) which was removed in pandas 2.0.0. A newer version of pandas is currently installed in the system. You must fix the environment so the script can run. **Requirement**: Do not modify the two pandas-related lines in the `main` function (the `pd.DataFrame()` and `df.append(...)` lines). You must resolve this by fixing the environment.
2. **Format Parsing Edge-Case**: Some lines in `/home/user/data.jsonl` contain invalid JSON with trailing commas (e.g., `{"id": 5, "value": 10,}`). The standard `json.loads` fails on these. You must modify `process.py` to gracefully handle or clean these specific trailing comma errors so that ALL valid records in the file are processed and counted.
3. **Race Condition**: The script uses a `ThreadPoolExecutor` to process lines concurrently, but it updates the global variable `total_valid_records` unsafely, leading to lost updates and inconsistent final counts. You must fix the race condition in `process.py` by introducing proper thread synchronization.

**Instructions**:
- Diagnose and fix the environment so the script runs.
- Modify `/home/user/process.py` to fix the parsing errors and the race condition.
- Run `/home/user/process.py`.
- Ensure the final count is written to `/home/user/output.txt`. Every record in `data.jsonl` contains a `value` key, so the final count should equal the total number of lines in the file.
- Do not change the overall logic of concurrent processing, just fix the bugs.
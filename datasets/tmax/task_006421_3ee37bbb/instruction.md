You have just inherited a fragile, undocumented data processing pipeline from a former developer. The pipeline is located at `/home/user/legacy_pipeline`. It consists of three Python scripts (`extractor.py`, `transformer.py`, `loader.py`) and a bash script (`run_pipeline.sh`) that runs them in sequence. Currently, the pipeline is completely broken and crashes midway through execution.

Your task is to debug and fix the pipeline by completing the following objectives:

1. **Handle Corrupted Input**: 
   The pipeline reads from `/home/user/legacy_pipeline/data/input.jsonl`. The file contains mostly valid JSON lines, but a few lines are corrupted and cause `transformer.py` to crash with a parse error. 
   Modify `/home/user/legacy_pipeline/transformer.py` so that instead of crashing, it catches the parsing exception, skips the corrupted line, and appends the exact raw, failing string to `/home/user/legacy_pipeline/data/rejected.txt`.

2. **Fix the Loader Crash**:
   Even if the transformer succeeds, `loader.py` crashes. You can find the stack trace of its last failure in `/home/user/legacy_pipeline/logs/loader_crash.log`. Analyze the stack trace to understand the bug (a logical error dealing with missing keys), and fix `/home/user/legacy_pipeline/loader.py` so it safely processes records. If a key 'target_value' is missing, default it to `0`.

3. **Reconstruct the Log Timeline**:
   The services log in completely different time formats:
   - `logs/extractor.log` uses UNIX Epoch timestamps (e.g., `1673856000 Extracting batch 1`)
   - `logs/transformer.log` uses ISO 8601 format (e.g., `2023-01-16T08:00:05Z Transformed batch 1`)
   - `logs/loader.log` uses YYYY/MM/DD HH:MM:SS format (e.g., `2023/01/16 08:00:10 Loaded batch 1`)
   
   Parse these three files and combine them into a single file at `/home/user/legacy_pipeline/logs/merged_timeline.txt`. 
   Every line in the merged file must be formatted as `<ISO-8601-UTC-Timestamp> <Original Message>` (e.g., `2023-01-16T08:00:00Z Extracting batch 1`), and the file must be sorted chronologically from oldest to newest. All logs were recorded in UTC.

4. **Run the Pipeline**:
   Once fixed, execute `/home/user/legacy_pipeline/run_pipeline.sh`. It must run to completion with exit code 0 and produce a final output file at `/home/user/legacy_pipeline/data/output.jsonl`.
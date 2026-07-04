You have inherited an unfamiliar, undocumented log processing codebase from a former developer. The system is designed to ingest logs from three interacting microservices (Alpha, Beta, and Gamma), reconstruct their causal timeline, and correct timestamp drift.

The codebase is located in `/home/user/log_pipeline/`. 
Inside, you will find:
- `service_alpha.log`, `service_beta.log`, `service_gamma.log`: Raw log files with drifted timestamps. Each log entry contains an `event_id` and sometimes a `parent_event_id` indicating causality (a parent event strictly occurred before its child).
- `reconstruct_timeline.py`: The primary Python script meant to parse the logs, resolve causal dependencies, adjust the drifted timestamps, and output a chronologically sorted merged timeline.

Currently, the pipeline is broken:
1. Running `python3 reconstruct_timeline.py` hangs indefinitely. You need to diagnose and fix a critical infinite recursion/loop termination bug in the causal resolution logic. The logs contain cyclic dependencies (e.g., retry loops) that the original developer did not handle correctly.
2. Even once the hang is fixed, the timeline reconstruction is naive and produces causality violations (where a child event appears before its parent in time).

There is also a proprietary, compiled evaluation tool left by the QA team at `/app/score_timeline`. It is a stripped binary that takes your output file and computes a "Causality and Drift Score" (0.0 to 100.0). 

Your objective is to:
1. Fix the infinite recursion in `/home/user/log_pipeline/reconstruct_timeline.py`.
2. Enhance the timestamp adjustment logic in the Python script so that parent events strictly precede child events, while minimizing the total shift from the original timestamps.
3. Run the script to generate `/home/user/log_pipeline/merged_timeline.json`.
4. Validate your output by running `/app/score_timeline /home/user/log_pipeline/merged_timeline.json`. 

You must iteratively refine your Python implementation until the binary reports a score of at least **95.0**.

The expected output format of `merged_timeline.json` is a JSON array of objects, sorted by the corrected timestamp:
```json
[
  {"service": "Alpha", "event_id": "req-1", "parent_event_id": null, "original_ts": 1620000000.100, "corrected_ts": 1620000000.100},
  ...
]
```
Ensure your final code is saved in `reconstruct_timeline.py` and the successfully scored JSON file is present at `/home/user/log_pipeline/merged_timeline.json`.
You are tasked with investigating a memory leak in a long-running data processing service. 

There is a local Git repository located at `/home/user/data_processor`. 
This repository contains a Python script `processor.py` that processes a stream of JSON records from `/home/user/data_processor/input.jsonl`. 

Recently, the service has been crashing due to out-of-memory (OOM) errors. The application processes records correctly, but we suspect it is mishandling corrupted input records (records missing certain required fields), leading to unbounded memory growth.

We know that the code tagged as `v1.0` is stable and does not leak memory. The bug was introduced somewhere between `v1.0` and the current `main` branch `HEAD`.

Your task is to:
1. Use git bisection (or manual commit traversal) to find the exact commit that introduced the memory leak.
2. Use interactive debugging or memory profiling (e.g., `tracemalloc`, `pdb`) on `processor.py` to identify the exact name of the global variable/list that is accumulating the corrupted records and causing the leak.
3. Once you have identified the bad commit and the leaking variable, create a report file at `/home/user/bug_report.txt` with exactly the following format:

```text
COMMIT_HASH: <full_40_character_commit_hash>
LEAKING_VAR: <exact_variable_name>
```

Ensure your final output exactly matches the keys above. Do not include extra text on those lines.
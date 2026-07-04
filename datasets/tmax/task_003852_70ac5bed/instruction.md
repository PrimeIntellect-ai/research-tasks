We are dealing with a broken log processing pipeline vendored at `/app/log_pipeline`. This pipeline consists of a Python log orchestrator, a compiled C binary used for fast log filtering, and a bash wrapper. 

Currently, the pipeline is failing to process a set of raw logs located at `/home/user/raw_logs.txt`. 

As a DevOps engineer, you need to debug this pipeline. Here are the issues we suspect:
1. **Dependency Conflict**: The Python wrapper script (`/app/log_pipeline/process.py`) requires specific versions of dependencies, but there is a conflict in the vendored `requirements.txt`. Resolve the conflict so the script runs.
2. **Infinite Loop/Recursion**: The Python script hangs during execution. Fix the recursion logic in the `parse_blocks` function in `process.py`.
3. **Binary Reversing**: The compiled C binary (`/app/log_pipeline/filter_bin`) requires a hidden magic string as an argument to activate the correct filtering mode. You'll need to analyze the binary to find this magic string and update the Bash wrapper (`/app/log_pipeline/run.sh`) to pass it.
4. **Query Result Debugging**: The output of the pipeline should be a JSONL file containing the parsed and filtered queries. 

Your goal is to successfully run `/app/log_pipeline/run.sh /home/user/raw_logs.txt /home/user/processed_logs.jsonl`.

The output file `/home/user/processed_logs.jsonl` will be evaluated against a reference set of parsed logs. 
You must achieve an F1 score of at least 0.95 when comparing the extracted query IDs to the ground truth.

Please complete the fixes and generate the final `processed_logs.jsonl` file.
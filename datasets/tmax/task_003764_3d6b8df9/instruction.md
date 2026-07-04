You are a DevOps engineer investigating a memory and task leak in our Python asynchronous microservices. We suspect that tasks are leaking under specific cancellation conditions. 

We have a proprietary log parsing library vendored at `/app/vendor/async-log-parser-0.2.1`. However, the previous maintainer left it in a broken state:
1. It fails to install due to a deliberate dependency conflict in its configuration.
2. It crashes with a traceback when parsing certain edge-case log lines (e.g., malformed lines without the standard separator).

Your tasks are as follows:

1. **Fix the vendored package**: Debug and fix `/app/vendor/async-log-parser-0.2.1` so it can be installed via `pip install -e .` and successfully parse log files without crashing.

2. **Statistical Anomaly Investigation**: We have provided two directories of log files for you to analyze:
   - `/home/user/corpora/clean/`: Logs from normal operations where resources are properly cleaned up.
   - `/home/user/corpora/evil/`: Logs from instances that suffered the cancellation leak.
   
   By analyzing these logs, you must identify the statistical anomaly that indicates a leak. Specifically, the leak occurs when asynchronous tasks are cancelled (`[CANCEL] Task <ID> interrupted`) but fail to emit their corresponding cleanup log (`[CLEANUP] Task <ID> resources released`). A log file should be considered "evil" (leaking) if it contains **5 or more** instances of a cancelled task ID that is NEVER subsequently cleaned up in that file.

3. **Create the Classifier**: Write a Python script at `/home/user/classifier.py` with the following CLI signature:
   `python3 /home/user/classifier.py <input_directory> <output_json_path>`
   
   The script must:
   - Iterate over all `.log` files in the given `<input_directory>`.
   - Use the fixed `async_log_parser` package to read the logs.
   - Output a JSON file at `<output_json_path>` where keys are the base filenames (e.g., `server_01.log`) and values are either the string `"clean"` or `"evil"`.

You must achieve 100% accuracy on both the clean and evil corpora. Do not hardcode the filenames; your script will be tested against a hidden set of logs following the exact same rules.
You are a DevOps engineer tasked with performing forensics on a crashed microservice. You have been given an application trace log file at `/home/user/app_trace.log` and an incomplete parsing script at `/home/user/trace_analyzer.py`. 

The log file contains JSON lines representing execution traces. Each trace has a `trace_id`, an optional `parent_id`, and a `message`. The script is supposed to reconstruct the full execution path for every trace in the log and write the results to a JSON file.

However, the logging system failed catastrophically. The log file is now filled with:
1. Corrupted, non-JSON lines (including null bytes and partial writes).
2. Cyclic references where a child trace claims its parent is a trace that actually depends on the child, creating an infinite loop in trace resolution.
3. Malformed `trace_id`s. Valid `trace_id`s strictly consist of the letter 'T' followed by exactly 3 digits (e.g., "T001").

The current script (`/home/user/trace_analyzer.py`) crashes due to `RecursionError` and `JSONDecodeError`. 

Your task is to debug and modify `/home/user/trace_analyzer.py` to:
1. Handle and recover from corrupted, non-JSON input lines gracefully (skip them entirely).
2. Fix the infinite recursion by detecting cycles in the `parent_id` chain. If a cycle is detected, or if a `parent_id` is missing from the parsed logs, skip processing that specific `trace_id`.
3. Implement assertion-based intermediate validation. Before adding any parsed log line to the processing dictionary, you MUST use Python's `assert` statement to verify that the `trace_id` strictly matches the required format ('T' + 3 digits). If the assertion fails, catch the `AssertionError` and skip that line.
4. Output the successfully resolved traces to `/home/user/clean_traces.json`. The output must be a valid JSON dictionary where the keys are the `trace_id`s and the values are the full trace strings formatted as `"Message 1 -> Message 2 -> Message 3"`.

When you are finished, you should be able to run `python3 /home/user/trace_analyzer.py` successfully and it should produce `/home/user/clean_traces.json`. Do not change the file paths.
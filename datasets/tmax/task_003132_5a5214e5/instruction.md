You are a Site Reliability Engineer (SRE) investigating intermittent crashes in a critical health monitoring service. 

Recently, the uptime monitoring system has been dropping metrics. You inspected the system and found that a background aggregation script is crashing with a `ZeroDivisionError` when processing certain edge-case payloads from monitored nodes.

You are provided with:
1. The aggregation script at `/home/user/health_aggregator.py`.
2. A snippet of the recent crash logs at `/home/user/logs/aggregator.log`.

Your objectives:
1. **Analyze** the log file and the source code of `/home/user/health_aggregator.py` to understand the root cause of the crash.
2. **Fuzz** the function: Write a Python fuzzing script (you can name it `/home/user/fuzzer.py`) that generates random JSON payloads to send to `health_aggregator.py` until it reliably triggers the `ZeroDivisionError`.
3. **Isolate the bug**: Once your fuzzer finds a crashing payload, save a minimal, valid JSON payload that triggers the bug to `/home/user/bug_trigger.json`. The payload must follow the schema expected by the script (a JSON object with a `"nodes"` array, where each node has `"id"` and `"metrics"`).
4. **Fix the codebase**: Modify `/home/user/health_aggregator.py` so that it handles the problematic mathematical condition gracefully. Specifically, if the divisor in `compute_score` evaluates to zero, the function should return `0` instead of raising an exception. Do not change the function signature or the rest of the logic.

Constraints:
- You must use standard Python 3.
- The `bug_trigger.json` file must be a valid JSON file that, when passed to the original script, causes a `ZeroDivisionError`.
- The fixed `health_aggregator.py` must print the expected output and exit with code 0 even when processing `bug_trigger.json`.
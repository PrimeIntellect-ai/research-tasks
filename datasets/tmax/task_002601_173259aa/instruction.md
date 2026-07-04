I need your help fixing a bug in a long-running telemetry processing service. We are using a vendored version of the `simplejson` Python package to parse incoming JSON payloads. However, the service keeps running out of memory and crashing after a few hours. 

We captured a crash dump and found that it happens when the service receives a specific type of corrupted JSON input over the network. I've narrowed down the issue to the vendored `simplejson` package located at `/app/simplejson-3.19.1`. 

Your task is to:
1. Use delta debugging/test minimization techniques on the sample of corrupted inputs I've provided in `/app/corrupted_samples.txt` to isolate the exact JSON structure causing the unbounded memory growth.
2. Fix the bug in the vendored `simplejson` source code located in `/app/simplejson-3.19.1/simplejson/` so that it correctly handles (raises a `simplejson.errors.JSONDecodeError`) the corrupted input instead of getting stuck in an allocation loop.
3. Create a wrapper script at `/home/user/parse_fuzz.py` that reads a JSON string from `stdin` and prints "SUCCESS" if it parses successfully, or "ERROR" if it raises a JSONDecodeError. If it encounters the memory leak loop, it will obviously hang.

The automated verification system will fuzz your `/home/user/parse_fuzz.py` script with thousands of mutated JSON strings and compare its stdout and exit codes against our secure reference implementation to ensure the memory leak is fixed and no valid JSON parsing behavior was broken.
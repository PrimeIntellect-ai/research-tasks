You are an SRE investigating an uptime monitoring service that recently crashed. The service's automated build pipeline is also currently failing due to a broken test related to payload parsing.

You have been provided with two files in your home directory (`/home/user/`):
1. `monitor_crash.dmp`: A simulated memory dump from the crashed process.
2. `test_uptime.py`: The failing test file for the payload decoder.

Your tasks are:
1. **Memory Dump Analysis & Encoding Troubleshooting**: 
   The memory dump contains a crash payload sandwiched between the ascii markers `[UPTIME_CRASH_DUMP_START]` and `[UPTIME_CRASH_DUMP_END]`. The data between these markers is a hex-encoded string. When unhexlified, it represents a JSON object encoded in a specific text encoding (not standard UTF-8, which is causing the current issues). 
   Extract the payload, correctly decode it to a JSON string, and save the formatted, decoded JSON to `/home/user/extracted_payload.json`.

2. **Build Failure Diagnosis**:
   Run `pytest /home/user/test_uptime.py`. You will see it fails with an encoding/serialization error. 
   Fix the `decode_payload` function inside `/home/user/test_uptime.py` so that it correctly decodes the hex string into a Python dictionary, allowing the test suite to pass.

Both the extracted JSON file and the fixed test file must exist and be correct for the task to be considered complete.
You are an on-call engineer at a climate tech company. It's 3 AM, and you've just been paged because the nightly data aggregation pipeline is crashing. 

The pipeline processes sensor logs in newline-delimited JSON (NDJSON) format. The processing script is located at `/home/user/processor.py` and it is reading a log file located at `/home/user/sensor_logs.ndjson`.

When running `python3 /home/user/processor.py /home/user/sensor_logs.ndjson`, the script crashes with a `ValueError`. The system logs indicate this crash happens intermittently based on specific sensor conditions.

Your task is to:
1. Investigate the cause of the crash in `/home/user/processor.py`. The crash occurs due to a format parsing edge case that is only triggered under a specific statistical condition (an anomaly in the recent sequence of temperature readings).
2. Use delta debugging/test minimization to isolate the absolute minimal sequence of lines from `sensor_logs.ndjson` required to reproduce the exact same `ValueError` crash. Save this minimal reproducible example to `/home/user/minimal_crash.ndjson`. (It should contain the minimum number of valid JSON lines from the original file needed to trigger the crash).
3. Fix the bug in a new file `/home/user/fixed_processor.py`. The fix should handle the parsing edge case by defaulting the problematic field to `-1` when it cannot be parsed as an integer, instead of crashing. The script should otherwise maintain its original logic and successfully process the entire `/home/user/sensor_logs.ndjson` file.

Verification Requirements:
- `/home/user/minimal_crash.ndjson` must exist, contain valid JSON lines from the original dataset, and running the original `processor.py` against it must reproduce the crash. It must be the minimal length possible.
- `/home/user/fixed_processor.py` must successfully process `/home/user/sensor_logs.ndjson` without crashing and print "Success".
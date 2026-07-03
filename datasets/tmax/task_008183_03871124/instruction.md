You are a Site Reliability Engineer investigating an intermittent outage in your team's uptime monitoring service. 

A proprietary, compiled Python module located at `/home/user/monitor.pyc` is responsible for parsing raw heartbeat data from external servers. Occasionally, the process crashes with a `RuntimeError`, bringing down the monitor. The original developer noted this behavior mimics an "unwrap panic" from an older Rust version of the tool when it encounters specific edge-case data, but the source code for `monitor.pyc` has been lost.

Your task:
1. Use standard Python forensic and disassembly tools to reverse engineer `/home/user/monitor.pyc` and identify the exact byte-sequence conditions that trigger the `RuntimeError`.
2. Construct a regression test script at `/home/user/regression_test.py`. This script must import the `monitor` module, construct a minimal bytes payload that triggers the crash, and call `monitor.process_heartbeat(payload)`. The script should catch the `RuntimeError` and print "REPRODUCED" to standard output.
3. Write the exact bytes payload you discovered into `/home/user/payload.txt` as a continuous hex-encoded string (e.g., `484541525442454154...`).

Ensure that your payload strictly satisfies all conditional checks in the bytecode to reach the exception.
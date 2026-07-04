You are a security researcher analyzing a suspicious data parser recovered from a malware command-and-control (C2) server. The parser, located at `/home/user/workspace/beacon_parser.py`, is used to decode incoming telemetry payloads. 

During initial analysis, we noticed the parser occasionally crashes when processing certain payloads, preventing us from analyzing the full C2 traffic dump. 

Your objectives are:
1. **Fuzzing & Delta Debugging:** We have a large crashing payload saved in `/home/user/workspace/crash_payload.txt`. Write a delta debugging script to minimize this payload to the absolute minimum number of comma-separated components that still triggers the exact same `ValueError: Checksum precision mismatch` or `IndexError: Malformed padding sequence` exceptions. Save the minimal crashing payload string to `/home/user/workspace/minimal_crash.txt`.
2. **Precision & Edge-Case Repair:** Analyze the source code of `/home/user/workspace/beacon_parser.py`. You will find two distinct bugs:
   - A floating-point precision error causing the checksum validation to fail incorrectly on valid telemetry data.
   - A format parsing edge-case where trailing empty padding components (caused by trailing commas or multiple consecutive commas) crash the parser.
   Fix both bugs directly in `/home/user/workspace/beacon_parser.py` so that it robustly handles floating-point summations (using an epsilon or `math.isclose`) and gracefully ignores empty padding segments without crashing.
3. **Regression Testing:** Create a comprehensive regression test suite at `/home/user/workspace/test_parser.py` using `unittest` or `pytest`. It must test the previously crashing minimal payload, verify the floating-point precision fix, and ensure format parsing handles edge-cases correctly.

**Success Criteria:**
- `/home/user/workspace/minimal_crash.txt` contains the minimized payload.
- `/home/user/workspace/beacon_parser.py` is patched, and running `python3 /home/user/workspace/beacon_parser.py --payload "0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,PAD,"` succeeds without throwing exceptions.
- `/home/user/workspace/test_parser.py` exists, tests the fixes, and returns a 0 exit code when executed.
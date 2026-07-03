You are debugging a failing build for a Python-based asynchronous network service. The integration tests are failing because the service leaks internal background tasks when a client disconnects unexpectedly or requests a specific URL, eventually causing resource exhaustion. 

You have been provided with artifacts from the latest failed CI build:
1. A network packet capture of the test traffic right before the crash: `/home/user/traffic.pcap`
2. A raw memory dump of the Python process at the time of the failure: `/home/user/crash_dump.bin`
3. The server source code: `/home/user/server.py`
4. The test runner script: `/home/user/test_build.py`

Your objectives:
1. **Analyze the Packet Capture:** Identify the exact HTTP GET request path that triggered the final error in the pcap file. Write *only* the path (e.g., `/example_path`) to `/home/user/crash_path.txt`.
2. **Analyze the Memory Dump:** The service writes a specific authentication flag into memory during initialization, but it doesn't log it. Extract this flag (which matches the format `FLAG_{...}`) from the raw memory dump `/home/user/crash_dump.bin`. Write the extracted flag to `/home/user/flag.txt`.
3. **Debug and Fix the Code:** Investigate `/home/user/server.py`. There is a bug where background tasks initiated during client connections are not properly cleaned up or cancelled when the connection closes. Use whatever debugging techniques you prefer (e.g., interactive debugging, print statements) to identify the leak. Fix the code in `/home/user/server.py` so that running `python3 /home/user/test_build.py` successfully prints `PASS` and exits with code 0.

Ensure that after your work:
- `/home/user/crash_path.txt` contains the correct HTTP path.
- `/home/user/flag.txt` contains the correct flag.
- `python3 /home/user/test_build.py` executes successfully without leaking tasks.
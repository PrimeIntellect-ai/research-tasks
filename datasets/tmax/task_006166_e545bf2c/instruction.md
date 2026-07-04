**PagerDuty Alert - 03:00 AM**
**Service:** `user-profile-svc` (Python)
**Alert:** Service crashed unexpectedly in production.
**Severity:** SEV-1

You are the on-call engineer. The `user-profile-svc` running on port 9000 crashed a few minutes ago. The upstream client service (written in Node.js) reported connection resets. 

A fellow engineer managed to grab a packet capture (`/home/user/incident.pcap`) of the traffic to port 9000 right when the crash occurred, before the container restarted. 

The server code is located at `/home/user/server.py`. 

Your tasks to resolve this SEV-1:

1. **Analyze the PCAP:** Inspect `/home/user/incident.pcap` to identify the exact malformed payload or request sequence that caused the Python server to crash.
2. **Create a Minimal Reproducible Example (MRE):** Write a Node.js script at `/home/user/mre.js` that connects to `127.0.0.1:9000` and sends the exact payload that caused the crash. Running this script against the original `server.py` should cause the server to crash.
3. **Fix the Bug:** Modify `/home/user/server.py` so that it safely handles this payload without crashing. It should instead return a JSON response `{"status": "error", "reason": "bad_request"}` when it encounters this specific issue, and keep running to serve future requests.
4. **Write a Regression Test:** Write a Python test script at `/home/user/regression_test.py` that:
   - Starts the fixed `server.py` as a subprocess.
   - Wait 1 second for the server to start.
   - Connects to the server and sends the poison payload.
   - Asserts that the response is `{"status": "error", "reason": "bad_request"}`.
   - Connects again and sends a valid payload (`{"action": "ping"}`) to assert the server is still alive and responds with `{"status": "pong"}`.
   - Exits with code 0 if all tests pass, or non-zero if the server crashes or returns the wrong response.
   - Cleans up (kills) the server subprocess before exiting.

Ensure your Node.js MRE script uses standard built-in modules (e.g., `net`). 
Do not change the server's listening host or port.
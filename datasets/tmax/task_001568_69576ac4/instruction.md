We are experiencing a regression in our internal authentication microservice. Recently, a developer made a series of commits, and now the service throws HTTP 500 errors when certain users try to authenticate. 

Your task is to debug, fix, and deploy the patched service.

Here is what you have:
1. `/home/user/auth_service/` - A git repository containing the Python HTTP service. The entrypoint is `server.py`. The bug was introduced somewhere in the last 200 commits.
2. `/home/user/traffic.pcap` - A packet capture of the traffic when the error occurred. Analyze this to identify the payload that triggers the failure.
3. `/home/user/crash.core` - A memory dump of the service at the time of the crash. The service requires an `X-API-Key` header for all requests. The key was loaded from an environment variable that is no longer documented, but it is present in this core dump. You must extract this key to test your fix.
4. `/app/bin/auth_oracle` - A stripped, pre-compiled C binary that the Python service wraps. It performs the actual token validation. 

Instructions:
1. Analyze the pcap to find the problematic request. You will notice it involves a specific input structure (hint: look at filenames or strings with spaces).
2. Extract the `X-API-Key` from the core dump.
3. Fuzz or trace `/app/bin/auth_oracle` to understand how it expects inputs to be formatted.
4. Locate the regression in the Python code in `/home/user/auth_service/server.py` and fix the bug. The bug is related to how the Python code passes arguments to the stripped binary.
5. Start the fixed service so it listens on `127.0.0.1:8888`. 

The automated verifier will send HTTP POST requests to `http://127.0.0.1:8888/verify` with the extracted `X-API-Key` and various payloads to ensure the regression is resolved. Leave the service running in the background.
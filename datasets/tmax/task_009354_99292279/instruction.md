You are a penetration tester investigating a local server that was recently compromised. You have extracted a web server access log, located at `/home/user/access.log`.

One of the log entries contains a malicious request with a custom-encoded payload in the query string (e.g., `?data=...`). Your analysis suggests the attacker used a simple encoding scheme: the payload is a hex-encoded string, which, when converted to bytes, was XORed with the key `0x42`.

Your objective is to:
1. Write a C++ program (`/home/user/decoder.cpp`) that reads `/home/user/access.log`, extracts the hex payload from the `data=` parameter, and decodes it using the `0x42` XOR key to reveal the attacker's backdoor credentials.
2. The decoded credentials will be in the format `password=<secret>`.
3. The server is currently running locally on port `8080`. The attacker left a backdoor endpoint somewhere in the range of `/api/backdoor_00` to `/api/backdoor_99`.
4. Write a script or program (C++ or bash) to automatically scan this endpoint range on `http://localhost:8080`. You must pass the decoded secret as a custom HTTP header: `X-Backdoor-Auth: <secret>`.
5. Only one endpoint will return a 200 OK status containing a JSON response with a "flag" field.
6. Extract the flag value and save it to `/home/user/flag.txt`.

Constraints:
- You must use C++ for the decoding portion of the task. 
- You may use standard Linux command-line tools (curl, bash) or C++ for the vulnerability scanning portion.
- Ensure your C++ code compiles with standard `g++`.
You are an incident responder investigating a compromised Linux container. We have identified a suspicious script located at `/home/user/suspicious_service.py` that is currently executing and running a hidden local web service. 

Your objective is to audit this service, extract its backdoor credentials, and verify the integrity of the script file. 

Perform the following tasks:
1. Identify the local port that the `/home/user/suspicious_service.py` process is currently listening on.
2. Write a Python script to send an HTTP GET request to `http://127.0.0.1:<port>/admin`. 
3. Inspect the HTTP response headers. The service will set a cookie named `Secret-Admin-Cookie`. Extract the value of this cookie.
4. Compute the SHA256 hash (lowercase hex digest) of the extracted cookie value.
5. Compute the MD5 hash (lowercase hex digest) of the `/home/user/suspicious_service.py` file itself.

Output your findings to a file exactly at `/home/user/report.txt` with the following format:
- Line 1: The SHA256 hex digest of the cookie value.
- Line 2: The MD5 hex digest of the `/home/user/suspicious_service.py` file.

Ensure your Python script correctly parses the cookie and performs the hashing. Do not modify or kill the running service.
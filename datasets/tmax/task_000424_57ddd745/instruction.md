You are acting as a security auditor for a company's internal network. During a recent architecture review, you discovered a proprietary, compiled authorization service used to validate incoming HTTP requests. 

The service binary is located at `/app/auth_checker`. It is a stripped ELF binary that reads raw HTTP requests from standard input (or from a file passed as the first argument) and exits with `0` if the request contains a valid, authorized administrator session, or `1` if authorization is denied or invalid.

We have captured a set of recent traffic, categorized into two directories:
- `/app/traffic/clean/`: Contains legitimate HTTP requests (both normal users and actual administrators).
- `/app/traffic/evil/`: Contains HTTP requests from a known malicious actor who successfully bypassed the authorization service to gain unauthorized administrator privileges without knowing the cryptographic MAC secret.

**Your Task:**
1. Reverse engineer or black-box analyze the `/app/auth_checker` binary to understand how it parses HTTP headers, specifically its custom authentication cookie/header mechanism, and identify the logical vulnerability that allows privilege escalation.
2. Inspect the HTTP requests in the clean and evil traffic directories.
3. Develop a Web Application Firewall (WAF) script in Python that detects the malicious exploitation technique while perfectly preserving legitimate traffic.

**Deliverable:**
Write a Python script at `/home/user/waf.py`. 
Your script must take exactly one command-line argument: the absolute path to a file containing a raw HTTP request.
- If the request is malicious (an attempt to exploit the parsing vulnerability), your script must print `EVIL` to standard output and exit with status code `1`.
- If the request is legitimate, your script must print `CLEAN` to standard output and exit with status code `0`.

Your script will be tested against the provided traffic directories, as well as an unseen holdout dataset. It must successfully categorize 100% of both the clean and evil corpora.
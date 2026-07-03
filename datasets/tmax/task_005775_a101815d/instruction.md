You are an incident responder investigating a potential breach on a web application. The attacker is suspected of exploiting a vulnerability by injecting malicious, encoded Python payloads via HTTP cookies.

You have been provided with a captured HTTP traffic log file located at `/home/user/traffic_logs.json`. This file contains a list of JSON objects representing HTTP requests. Each object has the following keys: `source_ip`, `method`, `headers`, and `cookies`.

Your task is to create a Python script at `/home/user/analyze_logs.py` to automate the scanning and vulnerability analysis of these logs. The script must perform the following steps:
1. Parse the `/home/user/traffic_logs.json` file.
2. Inspect the `cookies` dictionary of each request for the presence of the `X-Debug-Session` cookie.
3. If the cookie exists, extract its value. The attacker hides payloads by first Base64-encoding a Python script, and then URL-encoding the Base64 string. You must reverse this (URL-decode, then Base64-decode) to reveal the original Python payload.
4. **Safely** analyze the decoded Python payload. Do **not** execute the payload (`eval` or `exec`), as this is a severe security risk. Instead, use Python's built-in `ast` (Abstract Syntax Tree) module to parse the code.
5. Flag the request as malicious if the parsed AST contains:
   - An import statement (`Import` or `ImportFrom`) for the `os` or `subprocess` modules.
   - A function call (`Call`) to the built-in functions `eval` or `exec`.
6. For every malicious request found, extract the `source_ip`.
7. Write the flagged IP addresses to `/home/user/malicious_ips.txt`. Each IP should be on a new line. The list of IPs must be sorted in ascending string order and contain no duplicates.

Run your script to produce the output file.
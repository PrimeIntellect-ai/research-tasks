You are a network security engineer investigating a recent intrusion attempt. You have intercepted a web traffic log containing suspicious encoded requests targeted at a web application. 

The application currently uses a weak Content Security Policy (CSP):
`Content-Security-Policy: script-src 'self' https://cdn.vulnerable.com;`

Your task is to analyze the log, decode the attacker's payload, reconstruct an exploit generator, and enforce a secure policy.

Perform the following steps:

1. **Decode the Payload:**
   Read the traffic log located at `/home/user/traffic.log`. The log contains multiple HTTP GET requests. Attackers have hidden their payloads in the `?data=` query parameter, which is Base64 encoded.
   Write a Python script `/home/user/analyze.py` to parse the log, decode all `data` parameters, and identify the single payload that attempts to bypass the CSP using a JSONP callback endpoint on `https://cdn.vulnerable.com`. 
   Save the exact, decoded malicious HTML/Script payload to `/home/user/decoded_payload.txt`.

2. **Craft an Exploit Generator:**
   To test the vulnerability across other internal services, write a Python script `/home/user/craft_exploit.py`.
   This script must:
   - Accept a single command-line argument: a custom JavaScript payload (e.g., `console.log("xss")`).
   - Construct an HTML script tag that uses the `https://cdn.vulnerable.com/jsonp?callback=` endpoint to execute the provided custom JavaScript.
   - Base64 encode the entire HTML string.
   - Print *only* the Base64 encoded string to standard output.

3. **Enforce Content Security Policy:**
   Determine the best way to secure the application against this specific JSONP bypass while still allowing scripts from the same origin. 
   Write the corrected, strict CSP header to `/home/user/secure_csp.txt`. 
   The format in the file must be exactly: `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';`

Make sure all files are saved in `/home/user/` with the exact names specified.
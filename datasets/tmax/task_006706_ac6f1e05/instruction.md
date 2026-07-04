You are a network engineer tasked with investigating a recent security incident. An internal authentication service was targeted, and we suspect a rogue proxy intercepted traffic to manipulate the authentication flow. 

You have been provided with an investigation directory at `/home/user/investigation/` containing the following files:
1. `auth_logs.log`: A log file containing recent authentication attempts.
2. `intercepted_chain.pem`: The certificate chain captured during the incident.
3. `auth_server.py`: A local replica of the vulnerable authentication service.

Your objectives are:

**Phase 1: Certificate Chain Validation**
The file `intercepted_chain.pem` contains a chain of three certificates. A legitimate Root CA signed an intermediate certificate, which in turn signed the leaf certificate. However, the intermediate certificate in this chain is a known rogue proxy. 
Write a Python script (or use bash tools) to parse the certificate chain. Identify the Subject Common Name (CN) of the intermediate certificate (the one that is acting as the Issuer for the leaf, but is not self-signed). 
Write the exact Subject CN string of this rogue intermediate certificate to `/home/user/rogue_ca.txt`.

**Phase 2: Pattern Matching for Intrusion Detection**
Analyze the `auth_logs.log` file. The logs contain base64-encoded authentication tokens in the format `Bearer <base64_string>`. One of these tokens contains a malicious command injection payload wrapped in standard JSON. 
Identify the decoded payload that attempts to execute a shell command (look for a sequence containing `$(cat secret.txt)` or similar bash substitutions). 
Extract the fully decoded JSON string of the malicious payload and save it exactly as it appears (decoded) to `/home/user/payload.txt`.

**Phase 3: Authentication Flow Testing & Exploit Crafting**
The local service replica `auth_server.py` is vulnerable to the same payload. 
1. Start the server by running `python3 /home/user/investigation/auth_server.py &`. It will listen on `127.0.0.1:8080`.
2. Write a Python script `/home/user/exploit.py` that crafts a POST request to `http://127.0.0.1:8080/authenticate`.
3. The request must include an `Authorization` header containing the exact base64-encoded malicious token you discovered in Phase 2.
4. The server will respond with a JSON object containing a `"flag"` key if the exploit is successful.
5. Extract the flag from the response and write it to `/home/user/flag.txt`.

Ensure all output files (`rogue_ca.txt`, `payload.txt`, `flag.txt`) contain only the requested string without any surrounding whitespace, newlines, or quotes unless specified.
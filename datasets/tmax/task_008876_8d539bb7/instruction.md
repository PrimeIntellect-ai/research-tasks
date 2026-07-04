You are an incident responder investigating a suspected compromise on a Linux server. 

A custom web application is hosted in `/home/user/app/server.py`. We suspect the attacker exploited a vulnerability in the file upload mechanism to drop an obfuscated payload onto the system. 

Your objectives are to audit the code, analyze the logs, recover the payload, decode it, and craft a proof-of-concept (PoC) exploit to demonstrate the vulnerability.

Here is what you need to do:
1. **Audit the Application**: Review `/home/user/app/server.py` and identify the specific Common Weakness Enumeration (CWE) identifier for the vulnerability present in the file upload route.
2. **Locate the Payload**: Inspect the web server access log at `/home/user/logs/access.log` to determine the filename and location of the file dropped by the attacker.
3. **Decode the Payload**: The dropped file is a malicious script that has been encrypted using a cyclic XOR cipher. We know the encryption key is exactly **4 lowercase English letters**. You must brute-force the key, decrypt the file, and find the flag embedded inside the plaintext script. The flag format is `FLAG{...}`.
4. **Craft an Exploit**: Write a Python script at `/home/user/poc.py` that, when executed, sends a crafted HTTP POST request to the application (assuming it is running on `http://127.0.0.1:5000`). Your exploit must successfully upload a file such that it is saved exactly at `/home/user/success.txt` and contains the exact string `EXPLOITED`. 
5. **Report Findings**: Create a JSON report at `/home/user/report.json` with the following exact keys:
   - `"cwe_id"`: The standard CWE identifier for the vulnerability (e.g., `"CWE-79"`).
   - `"xor_key"`: The 4-letter lowercase key you brute-forced.
   - `"flag"`: The recovered flag string.

Constraints:
- You may use any standard tools or install libraries (like `requests` or `flask`) via `pip` if needed to test your scripts.
- The `server.py` is an unstarted Flask app. You may run it in the background if you wish to test your PoC locally. 

Your final evaluation will be based on the accuracy of `/home/user/report.json` and the successful execution of your `/home/user/poc.py` script.
You are an incident responder tasked with analyzing a potential breach on a web application. The application recently suffered an attack exploiting an open redirect vulnerability in its login flow. The attackers used this to redirect users to malicious phishing domains.

The web server's access logs were exfiltrated during the breach, but the original server was wiped. Fortunately, a backup system encrypted the access logs and stored them along with a configuration file. 

You need to perform the following steps:

1. **Decrypt the Logs**: The encrypted log file is located at `/home/user/evidence/access.log.enc`. It was encrypted using the Python `cryptography.fernet` module. The encryption key is stored as a base64 string within the configuration file located at `/home/user/evidence/config.ini`.
2. **Verify Integrity**: Once decrypted, verify the integrity of the raw log data. The SHA256 checksum of the original, unencrypted log file is stored in `/home/user/evidence/checksum.txt`. If the hash of your decrypted file does not exactly match the one in `checksum.txt`, your decryption process is flawed.
3. **Detect Intrusion Patterns**: Parse the decrypted log file to identify successful open redirect exploits. 
   - The vulnerable endpoint is `/login`.
   - The redirect parameter is `redirect`.
   - A *successful* open redirect exploit is defined as a `GET` request to the `/login` endpoint where the `redirect` parameter contains an absolute external URL (specifically starting with `http://` or `https://`), and the server responded with a `302` HTTP status code. 
   - Valid, non-malicious redirects use relative paths (e.g., `/dashboard` or `/profile`).
4. **Generate a Report**: Create a Python script that automates this analysis. The final output must be written to `/home/user/report.json` in the exact JSON format below.

Output format for `/home/user/report.json`:
```json
{
  "exploits": [
    {
      "ip": "<attacker_ip>",
      "target_url": "<malicious_url_extracted_from_redirect_parameter>"
    },
    ...
  ]
}
```

Ensure your Python script extracts all matching entries and writes the JSON report. You may write any necessary code, install standard tools (like `pip install cryptography`), or write bash scripts to aid in your task.
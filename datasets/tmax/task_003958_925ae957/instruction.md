You are a DevSecOps engineer responsible for policy enforcement and incident analysis. We have detected a rogue deployment on our internal network and need to analyze the artifacts left behind by the attacker to enforce our security policies.

You need to write a Python script at `/home/user/analyze_incident.py` that performs the following steps and outputs the results to a JSON file at `/home/user/enforcement_report.json`.

1. **Security Log Parsing**:
   Analyze the web server log file located at `/home/user/web_logs.txt`. Identify the IP address of the attacker who successfully uploaded a payload. The successful upload is indicated by a `POST` request to the `/api/v1/deploy` endpoint that resulted in a `201` HTTP status code.

2. **Reverse Engineering**:
   The attacker left behind a compiled Python bytecode file at `/home/user/rogue_auth.pyc`. Analyze this bytecode (you can use Python's built-in `dis` module or any decompilation technique) to extract a hardcoded MD5 hash string assigned to a variable named `SECRET_HASH`.

3. **Password Cracking**:
   Using the dictionary file located at `/home/user/passwords.txt`, perform a brute-force search to crack the MD5 hash extracted in the previous step. Find the plaintext password that corresponds to this hash.

4. **Certificate Validation**:
   The rogue service was running with a custom SSL certificate located at `/home/user/rogue_cert.pem`. Parse this certificate to extract the Common Name (CN) of the Issuer. 

Your script `/home/user/analyze_incident.py` must perform all these steps programmatically and write the final results to `/home/user/enforcement_report.json` with the following exact schema:

```json
{
  "attacker_ip": "<extracted_ip_address>",
  "hardcoded_hash": "<extracted_md5_hash>",
  "cracked_password": "<cracked_plaintext_password>",
  "cert_issuer_cn": "<extracted_issuer_common_name>"
}
```

Ensure your script is self-contained, executable via `python3 /home/user/analyze_incident.py`, and only uses standard Python libraries or tools available in a standard Linux environment (like `openssl` via `subprocess` if needed, though standard libraries are preferred).
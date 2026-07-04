You have been assigned to perform a security audit on a local internal reporting application. The application source code is located at `/home/user/app.py`. 

Your objectives are as follows:

1. **Integrity Verification**: Check the SHA-256 hash of `/home/user/app.py` against the expected hash found in `/home/user/manifest.txt`. Write exactly the word `VALID` or `INVALID` to `/home/user/integrity.log` based on the result.
2. **Vulnerability Exploitation**: The application uses a custom JWT implementation for its `/api/reports` endpoint. It is suspected to be vulnerable to an `alg=none` attack. You must craft a forged JWT to impersonate the `admin` user (who has the `"role": "admin"` claim). 
3. **Data Exfiltration**: Start the application in the background (`python3 /home/user/app.py &`) on port 8080. Use your crafted token to authenticate and fetch the restricted reports from `http://127.0.0.1:8080/api/reports`.
4. **Data Redaction**: The JSON response contains sensitive Social Security Numbers (SSNs) in the format `XXX-XX-XXXX`. You must process the retrieved JSON and redact all SSNs by replacing them entirely with the string `[REDACTED]`. Save the resulting JSON object to `/home/user/redacted_reports.json`. 

Ensure the final JSON is valid and retains the exact same structure as the original response, only with the SSN strings replaced.

Do not modify the original `app.py` file.
You are a Red Team operator managing an evasion-focused Command and Control (C2) redirector infrastructure. Your C2 stack consists of an Nginx reverse proxy, a Flask C2 backend, and a Redis session store. Currently, the infrastructure is broken, and you need to securely filter incoming web logs to protect your operational security.

Your task is divided into three stages:

**Stage 1: Multi-Service Infrastructure Fix**
The startup script `/app/start_infra.sh` brings up Nginx, Flask, and Redis. However, the end-to-end routing is failing. 
1. Fix the Nginx configuration located at `/app/nginx/nginx.conf` so that all HTTP requests on port 8080 are correctly proxied to the Flask backend. 
2. The Flask backend (`/app/c2/app.py`) is failing to authenticate to Redis. Update the environment variables or configuration file at `/app/c2/.env` so that Flask can securely connect to the Redis instance.
3. Secure the operational keys. Ensure all files inside `/app/c2/keys/` have permissions set to exactly `600` so only the owner can read/write them.

**Stage 2: Evasion Payload Filter (Bash)**
You must write a Bash script that acts as a log sanitiser and Blue Team probe detector. 
Create your script at `/home/user/c2_filter.sh`. It must accept exactly two arguments: an input log file path and an output log file path.
`bash /home/user/c2_filter.sh <input_file> <output_file>`

The input file will contain a list of requested URIs (one per line). Your script must process each URI according to the following rules:
1. **Drop Blue Team Probes**: Completely remove any URI that contains common vulnerability scanner payloads. Specifically, drop any line containing single quotes (`'`), double quotes (`"`), less-than (`<`), or greater-than (`>`) characters.
2. **Drop Unauthenticated Requests**: Drop any URI that does not contain the parameter `token=`.
3. **Preserve and Redact Clean Beacons**: If a URI passes the above checks, it is a valid beacon. To protect your C2 operations, you must perform sensitive data redaction. Replace the actual token value in the URI with `[REDACTED]` (e.g., `/?action=poll&token=abc123` becomes `/?action=poll&token=[REDACTED]`).
4. Write the surviving, redacted URIs to the `<output_file>`, maintaining their original relative order.

**Stage 3: Verification**
To verify your solution, ensure the infrastructure is running with your fixes by executing `/app/start_infra.sh`. 
Then, test your Bash script against the provided test files located in `/app/corpora/`.
You must ensure your script behaves perfectly before declaring the task complete.
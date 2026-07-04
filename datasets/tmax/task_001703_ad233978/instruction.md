You are a DevSecOps engineer tasked with enforcing policy as code and analyzing a recent security incident. We suspect attackers have bypassed authentication on our API gateway by exploiting a JWT implementation that accepts the `alg=none` (or `None`, `NONE`) signature bypass vulnerability.

You have been provided with an API gateway log file located at `/home/user/gateway.log`. Each line is a JSON object representing an HTTP request, containing the following fields: `timestamp`, `ip`, `path`, `auth_header`, and `status`.

Your objectives are:

1. **Log Parsing and Correlation:**
   Analyze `/home/user/gateway.log`. Find all unique IP addresses that made a successful request (`status` code `200`) using a JWT where the decoded header specifies the algorithm as "none" (in any case variation, e.g., "None", "none", "NONE"). Note that the `auth_header` is formatted as `Bearer <jwt_token>`.

2. **Network Policy Configuration:**
   Write a Bash script named `/home/user/block_ips.sh`. When executed, this script must parse `/home/user/gateway.log`, identify the malicious IPs from step 1, and generate a JSON network policy file at `/home/user/deny_policy.json`. 
   The generated JSON file must have the exact following structure, with the IP addresses sorted alphabetically:
   ```json
   {
     "blocked_ips": [
       "1.1.1.1",
       "2.2.2.2"
     ]
   }
   ```

3. **Authentication Flow Testing:**
   To prove the vulnerability exists to the development team, write a Bash script named `/home/user/craft_jwt.sh`. 
   - The script must accept a single argument: a username.
   - It must craft a JWT token using the `none` algorithm.
   - The decoded JWT Header must be exactly: `{"alg":"none","typ":"JWT"}`
   - The decoded JWT Payload must be exactly: `{"user":"<username>","role":"admin"}`
   - The script must print *only* the constructed JWT to standard output.
   - Remember that JWT parts are Base64Url encoded (URL-safe, without padding `=`), and an `alg=none` token still has three parts, but the signature part is empty (e.g., `header.payload.`).

Ensure all scripts are executable (`chmod +x`). Do not install any external tools; rely on standard Linux utilities like `jq`, `awk`, `grep`, `sed`, `base64`, etc.
You are a network engineer analyzing a suspected breach in your company's API infrastructure. The attacker may be exploiting a known JWT (JSON Web Token) vulnerability and operating over an endpoint with a lapsed SSL configuration. 

You have been provided with two sets of data in your home directory:
1. `/home/user/certs/` - A directory containing several PEM-formatted SSL certificates used by the API endpoints.
2. `/home/user/access.log` - A web server access log capturing recent traffic.

Perform the following tasks:

**Phase 1: TLS/SSL Certificate Management**
Analyze the certificates in `/home/user/certs/`. Identify the certificate that is currently expired. Extract its Subject Common Name (CN) and write it to `/home/user/expired_cert.txt`. The file should contain only the CN string (e.g., `api.example.com`).

**Phase 2: Log Parsing and Vulnerability Scanning**
The attacker is suspected of using the `alg: none` vulnerability to bypass JWT signature verification. 
Write a Bash script at `/home/user/scan_jwts.sh` that accomplishes the following:
1. Parses `/home/user/access.log` to extract all JWTs. Tokens are found in the log entries following the `Bearer ` keyword.
2. Decodes the header of each JWT to check if it uses the `"alg":"none"` or `"alg": "none"` algorithm. (Note: JWTs use base64url encoding).
3. For every vulnerable token identified, decode its payload and extract the value of the `sub` (subject) claim.
4. Output the extracted vulnerable subjects to `/home/user/vulnerable_subjects.txt`, with one subject per line, sorted alphabetically. 

**Requirements:**
- Your script `/home/user/scan_jwts.sh` must be written in Bash and be executable.
- Run your script to generate the final `/home/user/vulnerable_subjects.txt` file.
- Ensure all output files (`expired_cert.txt` and `vulnerable_subjects.txt`) are created exactly at the specified paths.
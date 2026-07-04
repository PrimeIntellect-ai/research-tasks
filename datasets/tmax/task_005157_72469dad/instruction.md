You are a compliance analyst tasked with generating a verifiable audit trail report. Your organization recently suffered a distributed brute-force attack. You need to correlate application authentication logs with firewall logs to identify specific threat actors, and then generate a cryptographically signed compliance token to prove the audit was completed.

You have been provided with two log files and a cryptographic secret in your home directory (`/home/user/`):
1. `/home/user/data/auth.log`: Contains application authentication logs.
2. `/home/user/data/ufw.log`: Contains Linux UFW (Uncomplicated Firewall) block logs.
3. `/home/user/config/jwt.secret`: Contains a plain text secret key used for signing tokens.

Your task is to write a Go program (you may save it as `/home/user/audit_tool.go` or similar) that performs the following steps:

1. **Log Parsing & Correlation**:
   - Parse `/home/user/data/auth.log` to find all IP addresses that had a "Failed login attempt".
   - Parse `/home/user/data/ufw.log` to find all IP addresses that were blocked (`[UFW BLOCK]`) specifically on destination port 8080 (`DPT=8080`).
   - Correlate the two sets to find IP addresses that appear in **both** categories (failed login AND blocked on port 8080).

2. **Token Generation**:
   - Generate a valid JWT (JSON Web Token) using HMAC-SHA256 (`HS256`).
   - The token must be signed using the exact secret string found in `/home/user/config/jwt.secret`.
   - The JWT payload (claims) must include:
     - `"role"`: A string exactly equal to `"compliance_analyst"`
     - `"audited_ips"`: A JSON array of strings containing the correlated IP addresses found in Step 1. The array must be **sorted alphabetically** (lexicographically).

3. **Output**:
   - Save ONLY the final raw JWT string to a file at `/home/user/audit_token.txt`. Do not include any extra whitespace, quotes, or newlines in this file.

**Log Formats**:
* `auth.log` lines look like: `2024-01-01T12:00:00Z ERR Failed login attempt user=admin ip=192.168.1.100`
* `ufw.log` lines look like: `Jan  1 12:01:00 host kernel: [UFW BLOCK] IN=eth0 OUT= MAC=... SRC=192.168.1.100 DST=10.0.0.1 ... DPT=8080 ...`

You may use standard Linux shell commands alongside your Go program, but the parsing logic and token generation must be executed. You will likely need to initialize a Go module and fetch a JWT package (e.g., `github.com/golang-jwt/jwt/v5`) in your workspace.
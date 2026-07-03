You are a security engineer tasked with rotating credentials and securing a legacy authentication microservice written in Go. The service has been flagged for suspicious activity, and you need to perform a quick incident response, code remediation, and deployment hardening.

Here is your detailed task breakdown:

**1. Code Auditing & Remediation (Go)**
The source code for the authentication service is located at `/home/user/app/auth_server.go`. 
- **Credential Rotation:** The code currently uses a hardcoded plaintext password (`"supersecret_legacy"`). Update the `loginHandler` to instead compare the incoming password against the SHA-256 hash of the new password: `"Str0ngR0tat1on!88"`. You must use `crypto/sha256` for the comparison (do not store the plaintext new password in the code).
- **CWE Identification & Fix:** The login flow contains an Open Redirect vulnerability (CWE-601) via the `next` query parameter. Attackers have been using this to redirect users to malicious domains. Fix the Go code so that it only permits relative redirects (the `next` path must start with a single `/` and must NOT start with `//`). If the validation fails, default the redirect to `/dashboard`.

**2. Intrusion Detection (Pattern Matching)**
We need to know who exploited the open redirect before you fixed it. 
Parse the web server access logs located at `/home/user/app/access.log`. 
Identify all unique IP addresses that successfully exploited the open redirect. A successful exploit is defined as an HTTP request to the `/login` endpoint where the `next` parameter contained an absolute URL (starting with `http://` or `https://`) AND the server responded with an HTTP 302 status code.
Save the list of unique IP addresses (one per line, sorted in ascending order) to `/home/user/compromised_ips.txt`.

**3. Process Isolation & Sandboxing**
To prevent future system-wide compromise, we want to run the microservice in an isolated environment.
Write a bash script at `/home/user/run_isolated.sh` that:
- Compiles the updated Go code (`/home/user/app/auth_server.go`) into an executable named `auth_server` in the same directory.
- Runs the compiled `auth_server` executable using the Linux `unshare` command to isolate it in a new, separate network namespace (so it cannot access the external internet, only the loopback interface). 
- Ensure the script is executable (`chmod +x`).

Complete all tasks directly in the terminal. Provide no setup files yourself; assume `/home/user/app` and its contents already exist.
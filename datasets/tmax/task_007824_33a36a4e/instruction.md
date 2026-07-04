You are a forensics analyst recovering evidence from a compromised host. You have been provided with a directory containing artifacts left behind by a custom, malicious authentication interceptor written in Go.

Your evidence directory is located at `/home/user/evidence/` and contains the following files:
1. `malware_server.go` - The source code of the attacker's custom TLS authentication interceptor.
2. `intercepted_cert.pem` - The rogue TLS certificate used by the malware to impersonate the system.
3. `traffic_logs.txt` - A log file containing Base64-encoded HTTP POST bodies of intercepted authentication attempts.

Your objective is to analyze these artifacts using standard Linux command-line tools and identify how the attacker's server was subsequently compromised by a third party.

Complete the following tasks:
1. Extract the "Common Name" (CN) from the Subject of the provided TLS certificate (`intercepted_cert.pem`).
2. Analyze `malware_server.go` to find a SQL injection vulnerability within its authentication handling logic. Note the exact line number where the raw, vulnerable SQL query string is constructed.
3. Decode the payloads in `traffic_logs.txt` and identify which payload successfully exploits the SQL injection flaw to bypass authentication as the user `admin` (assume the attacker needed a payload that comments out the password check).

Create a report file at `/home/user/findings.txt` with exactly three lines in the following format:
Line 1: [The TLS Certificate Common Name]
Line 2: [The line number in malware_server.go containing the vulnerable query string construction]
Line 3: [The exact, decoded POST body payload that exploits the SQLi]

Example of `/home/user/findings.txt`:
example.com
25
username=admin' OR 1=1 --&password=foo
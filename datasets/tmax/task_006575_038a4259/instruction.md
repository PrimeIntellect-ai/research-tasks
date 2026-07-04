You are a forensics analyst responding to a security incident on a compromised Linux host. The attacker managed to bypass authentication on an internal web application and drop a malicious payload. 

We have captured a log of JSON Web Tokens (JWTs) submitted to the application during the time of the breach. The log file is located at `/home/user/jwt_logs.txt`. One log entry per line.

Your investigation indicates that the attacker bypassed authentication by exploiting a known JWT vulnerability where the token specifies no cryptographic algorithm. Once authenticated, they embedded a base64-encoded ELF executable inside the token's payload under the key `"malware"`.

Your task is to:
1. Parse the JWTs in `/home/user/jwt_logs.txt` and identify the malicious token that exploits the `alg: none` (or equivalent) vulnerability.
2. Extract the base64-encoded payload from the `"malware"` field of that specific token.
3. Decode the base64 string to recover the malicious ELF binary.
4. Analyze the recovered ELF binary to determine its target architecture (the exact value of the "Machine:" field when using `readelf -h`).
5. Perform string analysis on the binary to locate the Command and Control (C2) server domain. The domain is known to end with the `.local` TLD (e.g., `something.local`).

Once you have recovered this information, create a JSON report at `/home/user/forensics_report.json` containing your findings. The JSON file must have exactly the following schema:

```json
{
  "malicious_line_number": 0,
  "elf_architecture": "exact machine string from readelf",
  "c2_domain": "extracted_domain.local"
}
```
*Note: `malicious_line_number` should be a 1-based integer representing the line number in `jwt_logs.txt` where the malicious token was found.*
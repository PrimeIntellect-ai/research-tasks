You are acting as a forensics analyst responding to a compromise on a Linux server. The attacker managed to bypass authentication, alter security configurations, and leave a local privilege escalation backdoor.

Your task is to analyze the artifacts left behind in the directory `/home/user/forensics/` and generate a forensic report.

Here is what you need to investigate:

1. **Authentication Bypass & Log Parsing**: 
   The web application was vulnerable to a JWT "algorithm: none" bypass attack. 
   Analyze the web server access logs located at `/home/user/forensics/server.log`. You need to find the specific HTTP request where the attacker successfully used a forged JWT with the `none` algorithm to bypass authentication. 
   Decode the JWT payload to extract the value of the `user` claim.

2. **Content Security Policy (CSP) & Integrity Verification**:
   The attacker modified one of the application's configuration files to weaken its Content Security Policy.
   You have a checksum manifest of the known-good application state at `/home/user/forensics/integrity.sha256`. 
   Verify the files in `/home/user/forensics/app/` against this manifest. Identify which file was maliciously altered. 
   Read the altered file (which contains CSP directives in JSON format) and extract the unauthorized, malicious domain that the attacker added to the `script-src` directive.

3. **Privilege Escalation Auditing**:
   The attacker dropped a privilege escalation tool in `/home/user/forensics/bin/`. You must audit this directory to find the specific binary/script that has the SUID (Set Owner User ID) bit set.
   Compute the SHA256 hash of this malicious SUID file.

**Deliverable**:
Using Python and/or shell commands, perform this analysis and create a final report at `/home/user/forensics/report.json`. The file must be valid JSON with the exact following structure and keys:

```json
{
  "attacker_user": "<the user claim extracted from the malicious JWT>",
  "malicious_csp_domain": "<the unauthorized domain added to script-src>",
  "privesc_file_hash": "<the lowercase SHA256 hex digest of the SUID file>"
}
```

Ensure all paths are absolute and correct as specified. Do not include any extra keys in the JSON report.
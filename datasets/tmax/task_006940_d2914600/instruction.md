You are a forensics analyst recovering evidence from a compromised Linux web server. The server's file system dump and web traffic logs have been mounted in your workspace at `/home/user/forensics/`. 

Your objective is to identify the privilege escalation vector the attacker left behind, analyze the web logs to find exfiltrated data in the HTTP headers/cookies, and generate a final forensic report.

Perform the following steps:

1. **Privilege Escalation Auditing:** The attacker planted a backdoor binary with the SUID bit set somewhere inside `/home/user/forensics/system_root/`. Locate this file. 
2. **Cryptographic Hashing:** Calculate the SHA256 checksum of the SUID binary you found.
3. **HTTP Header and Cookie Inspection:** The attacker exfiltrated sensitive data via an HTTP Cookie. Inspect the web logs located at `/home/user/forensics/logs/http_req.log`. Find the HTTP request that contains a suspicious cookie named `MalCookie`.
4. **Decoding:** The value of `MalCookie` is Base64 encoded. Decode this value to reveal the exfiltrated plaintext string.

Create a final report at `/home/user/forensics/evidence.txt` with the exact following format (replace the bracketed placeholders with your findings):

```
SUID_BINARY: <absolute_path_to_the_suid_binary>
SUID_HASH: <sha256_hash_of_the_binary>
EXFIL_DATA: <decoded_plaintext_from_MalCookie>
```

Ensure the file is formatted exactly as shown above with no extra lines or whitespace. You should use Bash commands and scripts to perform this analysis.
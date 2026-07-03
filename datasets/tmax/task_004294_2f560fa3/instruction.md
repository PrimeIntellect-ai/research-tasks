You are acting as a forensics analyst recovering evidence from a compromised web server. 

During the investigation, you discovered a strange, stripped Linux ELF executable left by the attacker at `/app/log_obfuscator`. Our preliminary analysis indicates that the attacker used this binary to continuously obfuscate and exfiltrate the web server's access logs and SSH audit logs to hide their tracks and steal session data. It appears to implement a custom, weak cryptographic algorithm to scramble text input.

Your task has two parts:

1. **Reverse Engineering & Equivalence:** 
You must reverse engineer the `/app/log_obfuscator` binary to understand the custom cryptographic cipher it uses. Using this knowledge, write a Go program that perfectly replicates the binary's behavior. 
- The binary reads from standard input (stdin) and writes the obfuscated data to standard output (stdout).
- Your Go program must do exactly the same.
- Save your Go source code at `/home/user/obfuscator_clone.go` and compile it to `/home/user/obfuscator_clone`.
Our automated systems will verify your work by running thousands of randomized fuzzing inputs through both the original `/app/log_obfuscator` and your `/home/user/obfuscator_clone` to ensure bit-exact equivalence.

2. **SSH Hardening & Remediation:**
The attacker also compromised the SSH configuration to maintain persistence. Review the backup configuration file at `/home/user/compromised_sshd_config`. 
- Identify the misconfigurations (e.g., weak ciphers, root login permitted, empty passwords allowed).
- Write a hardened version of this configuration to `/home/user/hardened_sshd_config` that disables root login, enforces Protocol 2, disables empty passwords, and restricts allowed MACs to `hmac-sha2-512,hmac-sha2-256`.

Good luck.
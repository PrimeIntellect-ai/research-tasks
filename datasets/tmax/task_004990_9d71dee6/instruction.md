You are a security auditor tasked with checking the file permissions of an SSH configuration directory.

There is a directory at `/home/user/ssh_audit` containing several SSH-related files. You need to write a C program at `/home/user/audit.c` that scans this directory and reports any files that violate the following strict permission rules:

1. **Public Keys**: Any file whose name ends with `.pub` must have permissions exactly `0644`.
2. **Config File**: A file named exactly `config` must have permissions exactly `0600` or `0644`.
3. **Authorized Keys**: A file named exactly `authorized_keys` must have permissions exactly `0600`.
4. **Private Keys**: Any file containing `id_rsa` or `id_ed25519` in its name (and not ending in `.pub`) is considered a private key and must have permissions exactly `0600`.

Any file in the directory that matches one of the above categories but has incorrect permissions must be reported. Files that do not match any of these categories should be ignored.

Your C program (or a wrapper shell script) must generate a final report at `/home/user/audit_results.txt`.
The report must contain one line for each non-compliant file in the format:
`filename:0XXX`
(where `0XXX` is the four-digit octal representation of the file's current permissions, e.g., `id_rsa:0644`).

The lines in `/home/user/audit_results.txt` must be sorted alphabetically by filename.

Complete the task by writing the C code, compiling it, executing it against `/home/user/ssh_audit`, and ensuring `/home/user/audit_results.txt` is correct.
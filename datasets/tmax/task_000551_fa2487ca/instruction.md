You are an external penetration tester conducting an offline audit of a client's extracted server artifacts. The client has provided a set of SSH keys and SSL certificates, but suspects some keys are poorly managed and the certificate chain is fragmented. 

You need to write a secure Bash script to perform the audit, adhering strictly to process isolation principles to prevent any accidental execution of malicious extracted code.

The artifacts are located in `/home/user/artifacts/` and include:
- `ssh_keys/`: A directory containing multiple SSH private keys (`key1`, `key2`, `key3`).
- `certs/`: A directory containing `root.pem`, `intermediate.pem`, and `leaf.pem`.

Your task is to write a Bash script at `/home/user/secure_audit.sh` that performs the following actions:
1. **SSH Hardening & Key Management Audit**: Iterate through the SSH private keys in `/home/user/artifacts/ssh_keys/`. Identify the single private key that is NOT protected by a passphrase. Extract the SHA256 fingerprint of this vulnerable key.
2. **Certificate Chain Validation**: The leaf certificate (`leaf.pem`) needs to be validated against the `root.pem` and `intermediate.pem`. You must construct the proper CA bundle and verify the leaf certificate.
3. **Process Isolation**: The certificate verification command (`openssl verify...`) MUST be executed inside an isolated sandbox using `bwrap` (Bubblewrap) within your Bash script. The sandbox must use the arguments `--unshare-all`, `--ro-bind / /`, and `--tmpfs /tmp` to ensure no network access and read-only filesystem access.

Your script must output the results to `/home/user/audit_log.txt` in precisely the following format:
- Line 1: The string `Vulnerable Key Fingerprint: ` followed by the SHA256 fingerprint of the unencrypted SSH key (e.g., `Vulnerable Key Fingerprint: SHA256:abcdef123...`).
- Line 2: The exact standard output of the sandboxed `openssl verify` command.

Requirements:
- Ensure `/home/user/secure_audit.sh` is executable.
- Run your script so that `/home/user/audit_log.txt` is generated.
- Do not install any new packages. The required tools (`openssl`, `ssh-keygen`, `bwrap`, `bash`) are already present on the system.
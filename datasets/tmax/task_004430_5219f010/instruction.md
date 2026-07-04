You are acting as a penetration tester analyzing a compromised Linux system. A background Python application is continuously processing data but is suspected of leaking sensitive credentials through its execution context. Furthermore, there are misconfigured security files and unverified data archives left by the system administrator.

Your objective is to perform the following security tasks using standard shell commands:

1. **Credential Extraction**: Find the running Python process executing `/home/user/data_processor.py`. It was launched with an `--api-key` argument. Extract this leaked API key (which is visible in the process's command-line arguments, e.g., via `/proc`) and save the exact key string to `/home/user/compromised_key.txt`.
2. **Access Control**: A private certificate key located at `/home/user/private.pem` has overly permissive file permissions. Secure this file by modifying its permissions so that only the owner has read and write access (no execution), and no one else has any access.
3. **Integrity Verification**: Verify the integrity of the data archive `/home/user/backup.zip` using its provided SHA-256 checksum file located at `/home/user/backup.zip.sha256`. If the checksum matches, write the exact word `VALID` to a new file named `/home/user/integrity_status.txt`. If it does not match, write `INVALID` to the file.

Ensure all output files are created in the `/home/user` directory exactly as specified.
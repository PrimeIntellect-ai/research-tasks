You are acting as a security engineer tasked with rotating certificate credentials for an application that uses certificate pinning. 

Before deploying the new certificate, you need to extract the currently pinned certificate hash from the application binary, generate the new certificate, and verify the integrity of the configuration backup.

Please write a Python script or use shell commands to perform the following steps:

1. **Binary Analysis**: The application binary is located at `/home/user/app_binary`. It is an ELF executable. The currently pinned TLS certificate SHA256 hash is stored as an ASCII string in a custom ELF section named `.cert_pins`. Extract this hash.
2. **TLS Certificate Management**: Generate a new 2048-bit RSA private key (`/home/user/new_key.pem`) and a self-signed X.509 certificate (`/home/user/new_cert.pem`). The certificate must be valid for 365 days and have the Common Name (CN) exactly set to `secure.example.com`. 
3. Calculate the SHA256 fingerprint (in lowercase hex) of the newly generated certificate. The fingerprint must be calculated over the DER-encoded binary form of the certificate.
4. **File Integrity Verification**: Calculate the SHA256 hash (in lowercase hex) of the backup file located at `/home/user/backup.tar.gz`.
5. **Reporting**: Create a JSON report at `/home/user/rotation_report.json` containing the extracted and calculated information. The JSON file must have exactly the following keys:
   - `"old_pinned_hash"`: The string extracted from the `.cert_pins` section of the binary. (Strip any trailing whitespace or null bytes).
   - `"new_cert_hash"`: The SHA256 hex digest of the new certificate's DER format.
   - `"backup_integrity_hash"`: The SHA256 hex digest of `/home/user/backup.tar.gz`.

Ensure your steps are fully completed and the JSON file is correctly formatted.
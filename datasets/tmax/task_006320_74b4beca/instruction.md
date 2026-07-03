You are a security engineer tasked with rotating credentials for a legacy backend system. A service recently failed to start due to a TLS certificate expiration and mismatch. 

Your task is to identify the failing service, discover its hardcoded certificate requirements, generate a replacement certificate, and secure the keys.

Perform the following steps using standard Linux terminal tools:

1. **Log Analysis:** Examine `/home/user/system.log` to identify the absolute path of the specific binary that reported a TLS handshake error.
2. **Binary Analysis:** Analyze the identified ELF binary to find the hardcoded Common Name (CN) it expects the TLS certificate to have. You are looking for an embedded string formatted exactly as `EXPECTED_CN=<target_cn>`.
3. **Certificate Generation:** Generate a new, self-signed X.509 certificate and an unencrypted RSA 2048-bit private key.
    - Save the certificate to `/home/user/certs/new_cert.pem`
    - Save the private key to `/home/user/certs/new_key.pem`
    - The Subject's Common Name (CN) must perfectly match the `<target_cn>` you extracted from the binary. Other subject fields can be left blank or default.
    - Set the certificate to be valid for 365 days.
4. **Access Control:** Apply strict file permissions to the newly generated credentials. The private key (`new_key.pem`) must have permissions set to `600`, and the public certificate (`new_cert.pem`) must have permissions set to `644`.
5. **Reporting:** Calculate the SHA256 fingerprint of the newly generated certificate. Write this fingerprint to `/home/user/rotated_fingerprint.txt` in the standard OpenSSL fingerprint format (e.g., `SHA256 Fingerprint=XX:XX:XX...`). Do not include any other text in this file.
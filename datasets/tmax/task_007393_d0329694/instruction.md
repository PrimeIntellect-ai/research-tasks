You are a security engineer tasked with rotating the embedded credentials of a legacy authentication agent. The agent is a compiled ELF binary that reads its client certificate, private key, and a cryptographic authorization token directly from a custom ELF section named `.secret_auth`. 

Your goal is to write and execute a Bash script at `/home/user/rotate_credentials.sh` that performs the end-to-end credential rotation and injects the new secrets into the binary.

Here are the specific requirements for the rotation:

1. **TLS Certificate Generation**: 
   - Generate a new RSA 2048-bit private key at `/home/user/new_agent.key`.
   - Generate a new self-signed X.509 certificate at `/home/user/new_agent.crt` valid for 30 days. The Subject must strictly be `CN=auth-agent`.

2. **Token Generation**:
   - Extract the SHA256 fingerprint of the newly generated certificate (format: `XX:XX:XX...`).
   - Read the master secret from `/home/user/master.key`.
   - Compute the HMAC-SHA256 of the certificate's SHA256 fingerprint string using the master secret. Save the resulting hex-encoded HMAC string to `/home/user/auth.token`.

3. **Payload Assembly**:
   - Create a single file at `/home/user/payload.bin` formatted exactly as follows:
     [HMAC_HEX_STRING]
     [CERTIFICATE_PEM_CONTENTS]
     [PRIVATE_KEY_PEM_CONTENTS]
   - (Ensure there is a newline after the HMAC string before the `-----BEGIN CERTIFICATE-----` block).

4. **ELF Binary Manipulation**:
   - You are provided with a base binary at `/home/user/base_agent`.
   - Copy it to `/home/user/rotated_agent`.
   - Inject the contents of `/home/user/payload.bin` into the `.secret_auth` section of `/home/user/rotated_agent`, replacing any existing contents in that section. Do not corrupt the rest of the ELF binary.

5. **Rotation Summary Log**:
   - Create a log file at `/home/user/rotation_summary.txt` containing exactly two lines:
     FINGERPRINT=<the_cert_sha256_fingerprint>
     TOKEN=<the_hmac_hex_string>

Ensure your Bash script completes all these steps successfully when run, leaving the final `rotated_agent` and `rotation_summary.txt` correctly populated in `/home/user/`.
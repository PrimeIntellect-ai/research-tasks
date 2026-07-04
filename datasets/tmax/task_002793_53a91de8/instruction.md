You are a security engineer performing a credential rotation. The senior engineer left an emergency audio message with the decryption passphrase.

Your tasks:
1. **Transcribe the Audio**: Listen to or transcribe `/app/voicemail.wav` to obtain the decryption passphrase.
2. **Payload Decoding & Certificate Validation (C++)**: 
   Write a C++ program at `/home/user/process_payload.cpp` that takes two arguments: the passphrase and the path to a payload file.
   The payload file (like the one provided at `/app/sample_payload.enc`) is a Base64-encoded file containing data encrypted with AES-256-CBC (the IV is the first 16 bytes of the decoded binary data, followed by the ciphertext). Use OpenSSL (`libcrypto`).
   
   The decrypted plaintext has the following custom format:
   - Line 1: The allowed SSH subnet (e.g., `10.0.5.0/24`)
   - The remaining lines contain one or more X.509 certificates in PEM format.
   
   Your C++ program must:
   - Decrypt the payload.
   - Extract the allowed SSH subnet.
   - Parse each PEM certificate and validate its chain against the Root CA located at `/app/root_ca.pem`.
   - Write the results to `/home/user/rotation_plan.txt` in exactly this format:
     ```
     Allowed Subnet: <subnet>
     Valid Certificates:
     <Subject Name of Valid Cert 1>
     <Subject Name of Valid Cert 2>
     ...
     ```
     *(Only include certificates that successfully validate against the Root CA).*

3. **SSH Hardening Script**: 
   Write a bash script `/home/user/harden_ssh.sh` that takes a path to an `sshd_config` file as an argument and modifies it in-place to:
   - Set `PasswordAuthentication no`
   - Set `PermitRootLogin no`

Ensure your C++ code compiles cleanly with `g++ -O2 process_payload.cpp -o process_payload -lcrypto -lssl`.
Your C++ implementation will be evaluated against a hidden, held-out set of payloads. It must correctly decrypt and validate all certificates.
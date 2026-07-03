You are a penetration tester analyzing a custom malware dropper found on a compromised Linux system. You have intercepted the dropper's configuration payload and its local certificate chain. Your task is to extract the payload and generate a firewall blocklist to secure the network.

You are provided with the following files in `/home/user/`:
1. `ca.crt` - The root Certificate Authority (PEM format).
2. `dropper.crt` - The malware's leaf certificate (PEM format).
3. `config.enc` - An encrypted configuration file containing a list of malicious IP addresses.
4. `config.md5` - A text file containing the MD5 hash of the decrypted configuration plaintext.

Perform the following steps using Python and standard Linux utilities:

1. **Certificate Validation & Fingerprinting:**
   Verify that `dropper.crt` was issued by `ca.crt`. Once verified, calculate the SHA256 fingerprint of the `dropper.crt` file (the digest of its DER-encoded representation). 

2. **Decryption:**
   The `config.enc` file is encrypted using AES-256-CBC. 
   - **Key:** The first 32 characters of the `dropper.crt` SHA256 fingerprint (in lowercase hex format), encoded as ASCII bytes.
   - **IV:** The first 16 bytes of the `config.enc` file.
   - **Ciphertext:** The remainder of the `config.enc` file.
   - **Padding:** PKCS7.
   Decrypt the configuration file to extract the plaintext.

3. **Integrity Check:**
   Compute the MD5 hash of the decrypted plaintext and ensure it matches the hash provided in `/home/user/config.md5`.

4. **Firewall Policy Generation:**
   The decrypted plaintext contains one IP address per line. Create a file named `/home/user/firewall_rules.sh`. For each IP address in the decrypted configuration, write exactly one line in the following format:
   `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
   Do not include a shebang (`#!/bin/bash`), comments, or any extra empty lines.

5. **Access Control:**
   Secure the generated script by setting its file permissions to exactly `0700` (readable, writable, and executable only by the owner).

Complete these steps in the terminal. You may write and execute Python scripts to assist you.
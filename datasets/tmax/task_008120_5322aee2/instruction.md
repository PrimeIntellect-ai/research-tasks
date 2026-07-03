You are a forensics analyst investigating a compromised Linux host. The attacker exploited a file upload handler susceptible to path traversal to drop a malicious payload and a command-and-control (C2) certificate.

Your objective is to write a Rust program that automates the recovery and decryption of the attacker's payload based on forensic artifacts.

**Step 1: Intrusion Detection via Pattern Matching**
You have been provided with the web server access log at `/home/user/server.log`. 
Write Rust code to parse this log file and identify the path traversal attacks. Specifically, look for `POST` requests to the `/upload` endpoint where the `filename` parameter contains the directory traversal sequence `../`.
The logs will reveal that the attacker uploaded two files into the `/home/user/compromised_data/` directory.

**Step 2: Certificate Chain Validation**
One of the uploaded files is an X.509 C2 certificate in PEM format. The attacker uses this certificate to derive decryption keys, but only if the certificate is signed by a specific compromised Certificate Authority (CA).
You are provided the compromised Root CA at `/home/user/rootCA.pem`.
Your Rust program must programmatically verify that the uploaded C2 certificate is signed by this `rootCA.pem`. (You may use Rust crates like `openssl` or call the `openssl` CLI tool from within your Rust code).

**Step 3: Payload Decryption**
If the certificate is validly signed by the Root CA, extract the Subject Common Name (CN) from the C2 certificate. The Common Name is a 64-character hexadecimal string representing a 32-byte AES-256 key.
The second uploaded file is the encrypted payload. It was encrypted using AES-256-GCM.
The structure of the encrypted binary file is:
- Bytes 0-11 (12 bytes): Initialization Vector (IV)
- Bytes 12 to (EOF - 16): Ciphertext
- Last 16 bytes: GCM Authentication Tag

Use the AES-256 key extracted from the certificate to decrypt the payload file. 

**Execution and Output**
Create your Rust project in `/home/user/forensics/`.
Your Rust program must execute these steps and write the final decrypted ASCII plaintext of the payload to `/home/user/decrypted_evidence.txt`.

Ensure your output file contains exactly the decrypted string and nothing else. You are free to use any standard or third-party crates (like `regex`, `aes-gcm`, `hex`, `openssl`) by defining them in your `Cargo.toml`.
You are an incident responder and forensics analyst investigating a compromised Linux server. The attacker deployed a custom command-and-control (C2) mechanism that hides malicious payloads inside standard-looking API requests.

You have been provided with the following artifacts extracted from the compromised host:
1. `/app/payload_decoder`: A stripped Linux binary used by the attacker to decode incoming payloads. 
2. `/app/rogue_cert.pem`: A rogue TLS certificate left behind by the attacker.
3. `/app/training_data/`: A directory containing several sample JSON API requests captured from the network logs. Some are benign, while others contain the attacker's C2 payloads.

Your objective is to write a standalone Rust command-line tool that acts as an automated vulnerability and payload scanner to classify files as clean or malicious. 

**Task Requirements:**
1. **Analyze the Binary:** Reverse engineer or interact with `/app/payload_decoder` to understand the payload obfuscation algorithm. The binary takes an obfuscated ASCII string via standard input and outputs the plaintext.
2. **Analyze the Certificate:** Extract the SHA-256 fingerprint of the provided `/app/rogue_cert.pem` file. The fingerprint should be represented as a continuous lowercase hex string (no colons).
3. **Payload Structure:** Inspect the JSON files in `/app/training_data/`. Each file contains a structure similar to:
   ```json
   {
     "timestamp": "2023-10-25T12:00:00Z",
     "metadata": { "source_ip": "192.168.1.5" },
     "data_payload": "<obfuscated_string>"
   }
   ```
4. **Identify Malicious Traffic:** A payload is considered malicious (EVIL) if and only if, after decoding `data_payload` using the algorithm you discovered, the resulting plaintext contains **both**:
   - The exact string `EXEC_C2:`
   - The SHA-256 fingerprint of the rogue TLS certificate.
5. **Build the Rust Scanner:** 
   - Initialize a new Rust project at `/home/user/detector`.
   - The tool must accept a single command-line argument: the absolute path to a JSON file.
   - It must decode the payload and evaluate it against the malicious criteria.
   - If the file is malicious, print `EVIL` to standard output and exit with status code `1`.
   - If the file is benign, print `CLEAN` to standard output and exit with status code `0`.
   - Compile your tool in release mode so the final executable is located at `/home/user/detector/target/release/detector`.

You may use standard Linux terminal tools (`xxd`, `ltrace`, `strace`, `openssl`, `strings`, etc.) to analyze the binary and certificate. Ensure your Rust program handles missing fields or invalid JSON gracefully by treating them as `CLEAN`.
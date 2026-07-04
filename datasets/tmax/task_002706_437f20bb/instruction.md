You are an incident responder investigating a compromised system. You have uncovered a suspicious custom command-and-control (C2) server source code located at `/home/user/IR_case/server.c`. The attacker left behind the CA certificates they used for mutual TLS authentication.

Your objective is to analyze the C2 server, compile it, and write an exploit in C to extract the hidden intelligence file from the running server.

Here are the specific details and requirements:

1. **Environment & Dependencies:**
   - All files are located in `/home/user/IR_case/`.
   - The server uses OpenSSL for mutual TLS. You may need to install necessary development packages (e.g., `libssl-dev` via `sudo apt-get` - *assume passwordless sudo is available for package installation if needed, though running standard compilers doesn't require root*).
   - Compile the server and run it locally on port `8443` (the port defined in the source).

2. **TLS Certificate Management:**
   - The attacker's CA key and certificate are located at `/home/user/IR_case/ca/ca.key` and `/home/user/IR_case/ca/ca.crt`.
   - The server's certificates are in `/home/user/IR_case/server/`.
   - The server enforces mutual TLS (mTLS) and verifies the client certificate.
   - You must generate a new client private key and a certificate signed by the provided CA. Save these as `/home/user/IR_case/client/client.key` and `/home/user/IR_case/client/client.crt`.

3. **Vulnerability Analysis & Exploit Crafting:**
   - Review `/home/user/IR_case/server.c`. The server receives a payload, base64 decodes it, and then XOR decodes it using the key `0x5A`.
   - The decoded data is mapped to a C structure. There is a memory corruption/struct overwrite vulnerability.
   - Write a C program at `/home/user/IR_case/exploit.c` that connects to `127.0.0.1:8443` using your generated client certificates.
   - Your exploit must craft a specific payload to overwrite the authentication flag in the server's memory, encode the payload properly (XOR with `0x5A`, then Base64), and transmit it over the TLS connection.

4. **File Integrity Verification:**
   - If your exploit is successful, the server will drop a file named `/home/user/IR_case/intel.txt`.
   - Calculate the SHA-256 hash of `/home/user/IR_case/intel.txt`.
   - Save the raw SHA-256 hash string (just the hex string, no filename or extra text) to `/home/user/IR_case/hash.txt`.

Successfully extracting the intel file and producing the correct hash proves you have mastered the attacker's C2 protocol.
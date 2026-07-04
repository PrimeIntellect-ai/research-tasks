You are a network security engineer investigating a proprietary application that is communicating over a non-standard port. You have intercepted a custom packet containing an encrypted payload. 

Your environment contains the following files in `/home/user/packet_analysis`:
- `parser.c`: A C program written by a junior engineer to parse the custom packet format and extract the encrypted payload. However, the program crashes with a segmentation fault/stack smashing when processing our captured packet due to a glaring memory corruption vulnerability.
- `capture.bin`: The captured binary packet.

Perform the following steps:

1. **Vulnerability Analysis & Fixing**: Analyze `parser.c` (you may use tools like `cppcheck` or manual code review). Identify and fix the buffer overflow vulnerability. Compile the fixed program to `/home/user/packet_analysis/parser_fixed` and run it against `capture.bin` to extract the payload to a file named `payload.enc`. Usage: `./parser_fixed capture.bin payload.enc`

2. **Cryptanalysis & Decryption**: The extracted `payload.enc` is encrypted using a weak repeating-key XOR cipher. Through traffic profiling, you know that the decrypted payload is a standard PEM-encoded TLS Certificate. Therefore, the plaintext is guaranteed to start with the string: `-----BEGIN CERTIFICATE-----`.
Write a C program named `decrypt.c`, compile it, and use it to perform a known-plaintext attack to recover the XOR key. Use the recovered key to decrypt `payload.enc` and save the resulting plaintext certificate to `/home/user/packet_analysis/extracted.crt`.

3. **TLS Certificate Management**: Using `openssl`, extract the SHA-256 fingerprint of the decrypted certificate. Save ONLY the exact hex fingerprint string (e.g., `XX:XX:XX...`) to `/home/user/packet_analysis/fingerprint.txt`.

Ensure your C code compiles without warnings and handles memory safely.
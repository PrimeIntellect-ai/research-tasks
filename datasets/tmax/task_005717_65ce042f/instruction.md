You are a forensics analyst investigating a compromised Linux host. You have secured a directory containing evidence at `/home/user/evidence/`. Inside this directory, you will find:
1. `dropper.elf`: The malicious executable recovered from memory.
2. `stolen_data.enc`: An encrypted file exfiltrated by the malware.
3. `known_plaintext.bin`: A file containing the first 12 bytes of the original unencrypted data of `stolen_data.enc`.

Your objective is to fully reverse-engineer the attack, extract the malware's cryptographic material, crack the encryption, and recover the stolen data.

Follow these phases:

**Phase 1: Binary Analysis and Certificate Extraction**
The malware binary `dropper.elf` contains a hidden ELF section named `.evil_cert`. This section contains a PEM-formatted X.509 certificate chain used by the malware's C2 server.
- Extract the raw contents of the `.evil_cert` section and save it to `/home/user/chain.pem`.
- Validate the certificate chain. Extract the Common Name (CN) of the **Root CA** (the issuer of the top-level certificate in the chain) and save this exact string to `/home/user/root_ca_cn.txt`.

**Phase 2: Cryptanalysis and Decryption (C++)**
The malware encrypts `stolen_data.enc` using a custom XOR stream cipher powered by a 32-bit Linear Congruential Generator (LCG).
The LCG formula is: `State_{n+1} = (1103515245 * State_n + 12345) mod 2^32`
For each byte of plaintext, the cipher extracts the *most significant byte* (bits 24-31) of the current 32-bit `State_n`, XORs it with the plaintext byte to produce the ciphertext byte, and then advances the state to `State_{n+1}`.

The initial seed (`State_0`) is a 32-bit integer, which serves as the encryption key.
- Write a C++ program at `/home/user/crack.cpp` that implements a Known-Plaintext Attack using `known_plaintext.bin` and the first 12 bytes of `stolen_data.enc` to recover the 32-bit initial seed (`State_0`).
- Your C++ program must then use this recovered seed to decrypt the entirety of `stolen_data.enc`.
- Compile your program as `/home/user/crack_cipher` (e.g., using `g++ -O2 /home/user/crack.cpp -o /home/user/crack_cipher`).
- Execute your compiled C++ program to decrypt the file and save the output to `/home/user/decrypted_data.txt`.

**Constraints and Verification:**
- You must use C++ to crack the cipher and decrypt the data.
- Ensure your C++ program is self-contained and compilable with standard g++.
- Automated tests will verify the existence and exact contents of `/home/user/chain.pem`, `/home/user/root_ca_cn.txt`, `/home/user/crack.cpp`, and `/home/user/decrypted_data.txt`.
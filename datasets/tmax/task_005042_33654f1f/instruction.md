You are a forensics analyst responding to a compromised Linux host. The attackers have encrypted a critical system log and left behind the encryption utility they used. Your job is to reverse engineer their utility, crack the encryption, and recover the exfiltrated data indicator.

Here is the situation:
1.  **`/home/user/case_notes.txt`** contains notes from the initial triage team. It states that all encrypted files start with a known plaintext header: `CRIME_LOG_START{v1.0}\n`
2.  **`/home/user/encryptor`** is the compiled ELF binary the attackers used to encrypt the files. It has been stripped of debug symbols.
3.  **`/home/user/evidence.bin`** is the encrypted log file we need to recover.

Your analysis objectives:
1.  **Reverse Engineer:** Disassemble and analyze `/home/user/encryptor`. The attackers used a custom Linear Congruential Generator (LCG) as a stream cipher. You need to identify the LCG multiplier, increment, and how the pseudo-random byte is extracted for the XOR operation. The state is a 32-bit unsigned integer.
2.  **Cryptanalysis:** Using the known plaintext header from the case notes, write a C program at `/home/user/decryptor.c` to perform a known-plaintext attack. Your program must brute-force the 32-bit initial seed used to encrypt `/home/user/evidence.bin` and then decrypt the entire file.
3.  **Recover & Hash:** Decrypt the file and save the plain text to `/home/user/decrypted.log`. Inside this log file, there is a line starting with `FLAG: `. Extract the exact string following `FLAG: ` (ignoring leading spaces and the trailing newline).
4.  Compute the SHA-256 checksum of that exact flag string and write the resulting hex hash into a single line in `/home/user/solution.txt`.

Constraints & Guidelines:
- You must write the brute-force tool in C to ensure it completes in a reasonable time.
- All files should be created and manipulated in `/home/user`.
- Ensure `/home/user/solution.txt` contains *only* the 64-character lowercase SHA-256 hash.
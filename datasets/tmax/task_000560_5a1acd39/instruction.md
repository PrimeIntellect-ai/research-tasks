You are a forensics analyst responding to a compromised Linux host. The attacker left behind a suspicious binary and tampered with system files. A snapshot of the compromised process's command-line arguments was captured before it terminated.

Your objective is to investigate the breach, reverse engineer the attacker's tool, and recover the injected payload.

**Environment Setup:**
All evidence is located in `/home/user/evidence/`.
- `/home/user/evidence/system_files/` contains copies of various system configuration files.
- `/home/user/evidence/checksums.txt` contains the known-good SHA256 hashes of these files before the breach.
- `/home/user/evidence/dropper.bin` is the malicious executable found on the system.
- `/home/user/evidence/proc_cmdline.log` contains the exact `/proc/[pid]/cmdline` contents of the dropper when it was running.

**Your Tasks:**

1. **File Integrity Verification:**
   Determine which file in `/home/user/evidence/system_files/` was tampered with by checking the files against `/home/user/evidence/checksums.txt`. 
   Write the base name of the tampered file (e.g., `config.ini`) to `/home/user/tampered_file.txt`.

2. **Reverse Engineering & Disassembly:**
   Analyze `/home/user/evidence/dropper.bin`. You may use tools like `objdump` or `strings`. The binary takes a payload file and an integer key as arguments, and applies a custom algorithmic obfuscation to hide an injected payload. 
   Analyze the command-line arguments in `/home/user/evidence/proc_cmdline.log` to determine the exact key the attacker used when running the dropper on the tampered file.

3. **Algorithmic Recovery in C++:**
   The tampered file contains a block of hex-encoded ciphertext injected at the end of the file between `===BEGIN PAYLOAD===` and `===END PAYLOAD===`.
   Based on your reverse engineering of `dropper.bin`, write a C++ program at `/home/user/recover.cpp` that implements the reverse of the obfuscation algorithm. 
   Compile and run your C++ program to decode the ciphertext using the key found in the command-line log.

4. **Extraction:**
   The decrypted payload contains a malicious SSH public key meant to establish a backdoor.
   Save the fully decrypted SSH public key string to `/home/user/decrypted_payload.txt`.

Ensure your C++ code compiles with `g++ /home/user/recover.cpp -o /home/user/recover`. The final output files `/home/user/tampered_file.txt` and `/home/user/decrypted_payload.txt` must contain exactly the specified information with no extraneous text.
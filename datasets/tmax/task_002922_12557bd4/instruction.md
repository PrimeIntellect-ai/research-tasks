You are a forensics analyst investigating a compromised host. The attacker exfiltrated data by exploiting a custom authentication daemon (an ELF binary located at `/app/auth_daemon`) that behaves similarly to a JWT service but critically fails to validate signatures when a specific `alg=none`-style bypass flag is set in the header. Once bypassed, the daemon processes malicious payloads containing shell injections and XSS vectors. 

Your task consists of three phases:

**Phase 1: SSH Key Recovery & Audio Forensics**
The attacker left behind an encrypted SSH private key (`/app/compromised_id_rsa`) and an audio recording of a VoIP intercept (`/app/intercept.wav`). 
1. Transcribe the audio file to recover the spoken password.
2. Decrypt the SSH key using this password.
3. Output the decrypted PEM key to `/home/user/decrypted_id_rsa` and ensure it has the correct permissions for SSH usage (0600).

**Phase 2: Binary Analysis**
Analyze the `/app/auth_daemon` ELF binary. Determine how it parses incoming JSON payloads and identify the exact injection vectors it is vulnerable to when the signature bypass is used. (Hint: look for how it handles the `cmd_exec` and `user_profile_xss` fields).

**Phase 3: C++ Payload Sanitizer**
Write a C++ program that acts as a strict sanitizer for these captured payloads. Your program must read a JSON payload from standard input and determine if it is malicious (contains injection/XSS attempts targeting the daemon) or clean.
1. Create your C++ source file at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
2. The program must return exit code `1` (reject) if the payload is malicious, and exit code `0` (accept) if the payload is clean.
3. The program must be robust and run without crashing.

We will test your compiled `/home/user/sanitizer` against a large adversarial corpus of payloads. It must correctly reject 100% of the malicious payloads and accept 100% of the clean payloads.
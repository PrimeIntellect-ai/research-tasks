You are a forensics analyst investigating a compromised Linux host. The attacker managed to exfiltrate data by blending malicious Command & Control (C2) beacons into the system's Content Security Policy (CSP) violation logs and TLS certificate metadata streams. 

During the investigation, you recovered a stripped, UPX-packed binary at `/app/beacon_gen`. We suspect the attacker used this tool to generate their malicious log entries. We also recovered a large dump of mixed logs, which we have partially triaged into two directories for your analysis:
- `/home/user/evidence/clean/`: Known legitimate CSP logs and TLS metadata.
- `/home/user/evidence/evil/`: Confirmed attacker-generated C2 beacons.

Your objective is to build a robust, standalone classifier in Go that can automatically distinguish between clean logs and attacker beacons based on the cryptographic signature or encoding scheme implemented by `/app/beacon_gen`.

Tasks:
1. Reverse-engineer `/app/beacon_gen` to understand how it signs or structures the "evil" logs. You may use tools like `strings`, `objdump`, or `gdb` (which are preinstalled). 
2. You will likely notice the binary uses a specific hashing or cryptographic MAC operation with a weakly derived key or hardcoded seed. You may need to perform a brief brute-force search or cryptanalysis to recover this key/seed.
3. Write a Go program at `/home/user/classifier.go` and compile it to `/home/user/classifier`.
4. Your compiled Go classifier must accept a single command-line argument (the absolute path to a log file to inspect).
5. The classifier must output an exit code of `0` if the file is a legitimate, clean log.
6. The classifier must output an exit code of `1` if the file contains the attacker's C2 signature or tampering.

Ensure your code handles malformed JSON safely and cleanly. The automated verification suite will test `/home/user/classifier` against thousands of unseen files.
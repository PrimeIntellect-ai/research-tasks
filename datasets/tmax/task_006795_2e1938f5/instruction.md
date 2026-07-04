You are a penetration tester performing a vulnerability assessment on a compromised host. You have discovered a proprietary logging system that the attackers are using to hide their intrusion detection logs. 

You found the source code for their encryption tool at `/home/user/encryptor.rs` and an encrypted log file at `/home/user/logs/encrypted_log.bin`. 

The attackers used a custom Linear Congruential Generator (LCG) to generate a pseudo-random keystream, which is then XORed with the plaintext log. You know the following:
1. The plaintext log ALWAYS begins with the exact string: `[SECURE_LOG_V1]`
2. The LCG seed used for the encryption is a 16-bit unsigned integer (between 0 and 65535).
3. The encryption algorithm parameters (Multiplier, Increment, Modulus) are visible in the provided `encryptor.rs` source code.

Your tasks are to:
1. Perform a known-plaintext attack / brute-force cryptanalysis to recover the 16-bit seed used to encrypt `/home/user/logs/encrypted_log.bin`.
2. Write a Rust program at `/home/user/decryptor.rs` that decrypts the log file and saves the plaintext to `/home/user/logs/decrypted_log.txt`.
3. Analyze the decrypted log using pattern matching. The log contains multiple lines. Find all lines containing the string `[ALERT] MALWARE_SIGNATURE_MATCH`.
4. Extract the IP addresses associated with these specific alerts. The log lines are formatted like: `... [ALERT] MALWARE_SIGNATURE_MATCH detected from IP: 192.168.1.55 ...`
5. Save the extracted IP addresses (one per line, sorted alphabetically, unique only) to `/home/user/flag.txt`.

Ensure your final output is strictly the list of IP addresses in `/home/user/flag.txt`.
You are a forensics analyst investigating a compromised Linux host. You have discovered a rogue binary left by the attacker, an encrypted evidence file, and a TLS certificate used for data exfiltration. 

Your investigation reveals the following assets:
1. `/home/user/malware`: A compiled Rust binary used by the attacker.
2. `/home/user/evidence.enc`: A system log file that the attacker encrypted using the malware. The encryption is a simple byte-by-byte XOR against a hardcoded string key.
3. `/home/user/attacker.pem`: A TLS certificate the attacker used to establish a secure C2 channel.

Your objective is to recover the encrypted evidence and identify the attacker's infrastructure. Perform the following steps:
1. **Reverse Engineering**: Analyze the `/home/user/malware` binary using standard shell tools (e.g., `strings`) to find the hardcoded XOR key. You know the key starts with the prefix `KEY_`.
2. **Decryption**: Write a Rust program at `/home/user/decrypt.rs` that reads `/home/user/evidence.enc`, performs a byte-by-byte XOR decryption using the recovered key (repeating the key cyclically as needed), and outputs the decrypted text. Run your program to get the plaintext.
3. **Certificate Analysis**: Extract the Common Name (CN) from the Subject field of `/home/user/attacker.pem` using standard OpenSSL commands.
4. **Reporting**: Create a final report at `/home/user/report.txt` with exactly the following format:

```
Decrypted Evidence: [INSERT DECRYPTED TEXT HERE]
Attacker CN: [INSERT EXTRACTED CN HERE]
```

Ensure your Rust script is compilable with the standard `rustc` compiler and that your final report matches the exact format requested.
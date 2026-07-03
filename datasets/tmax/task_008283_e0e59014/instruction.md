You are an incident responder investigating a compromised Linux host. We discovered a suspicious data dump `/home/user/exfil.enc` that contains encrypted HTTP traffic exfiltrated by a custom malware beacon.

Through earlier reverse engineering of the malware, we found that it encrypts data using a repeating XOR cipher. The XOR key is a 4-byte array derived from a 4-digit PIN (0000 to 9999). 

The key derivation logic in the malware's Rust source code is equivalent to:
```rust
let pin: u32 = /* 4-digit PIN */;
let key: [u8; 4] = (pin * 1337).to_be_bytes();
```

We know that the decrypted payload contains raw HTTP request headers, meaning the decrypted file will start with the string `"GET "`.

Your task:
1. Write a Rust program in `/home/user/decryptor/` (you will need to initialize a cargo project) that brute-forces the 4-digit PIN.
2. Use the correct PIN to completely decrypt `/home/user/exfil.enc`.
3. Inspect the decrypted HTTP headers and extract the value of the `X-Exfil-Auth` header.
4. Write ONLY the extracted value of the `X-Exfil-Auth` header to `/home/user/flag.txt` (without any trailing whitespace or newlines).

Work efficiently. The brute-force space is small, but you must implement the decryption and header parsing correctly.
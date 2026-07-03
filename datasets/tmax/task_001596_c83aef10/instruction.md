You are a forensics analyst investigating a compromised Linux host. The attacker left behind a suspicious executable file located at `/home/user/suspicious.elf`. 

Your initial triage indicates that the attacker hid exfiltrated evidence inside this binary. Specifically, the evidence is encrypted and stored in a custom ELF section named `.maldata`. 

Your task is to:
1. Extract the raw binary contents of the `.maldata` section from `/home/user/suspicious.elf`.
2. Write a C++ program at `/home/user/recover.cpp` that reads this extracted binary data and performs a brute-force attack to decrypt it. The encryption algorithm used by the attacker is a single-byte XOR cipher (the key is a single byte between `0x00` and `0xFF`).
3. The decrypted data contains a specific pattern. You must search the brute-forced outputs for a string that matches the format `FLAG{...}` (where `...` is a combination of alphanumeric characters and underscores).
4. Once your C++ program finds the correct key and decrypts the flag, it should write ONLY the exact flag string (e.g., `FLAG{example_flag}`) to a file named `/home/user/flag.txt`.

Constraints:
- You must use C++ to write the brute-force decryption program. You may use standard shell utilities (like `objcopy`, `readelf`, etc.) to analyze the ELF file and extract the custom section.
- Do not leave any background processes running.
- Ensure the final output file `/home/user/flag.txt` contains exactly the flag and nothing else (no newlines).
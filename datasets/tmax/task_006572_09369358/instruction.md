You are acting as a penetration tester examining an extracted artifact from a target system. You have been provided with an evidence archive and its checksum. Your goal is to reverse engineer the local authentication logic and recover a target PIN.

Perform the following steps:
1. Verify the integrity of the evidence archive `/home/user/evidence.zip` against the expected SHA256 hash provided in `/home/user/evidence.zip.sha256`. If the hash does not match, write exactly the word `CORRUPTED` into `/home/user/cracked_pin.txt` and stop.
2. If the integrity check passes, extract the contents of `/home/user/evidence.zip` into `/home/user/evidence/`.
3. Inside the extracted directory, you will find a compiled Python script `login_validator.pyc` and a text file `target_hash.txt` containing a single SHA256 hash.
4. The `login_validator.pyc` contains a function that validates a 4-digit numeric PIN. Disassemble or decompile this file to understand the specific hashing algorithm, including any salts or transformations applied to the PIN before hashing.
5. Write a Python script to brute-force the 4-digit numeric PIN (from 0000 to 9999) that produces the hash found in `target_hash.txt`.
6. Once you have successfully cracked the PIN, write the 4-digit PIN to `/home/user/cracked_pin.txt`.

Ensure your final answer in `/home/user/cracked_pin.txt` contains only the 4-digit numeric PIN, with no extra whitespace or characters.
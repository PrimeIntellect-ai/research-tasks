You are a security engineer tasked with rotating database credentials. The previous engineer used an insecure hashing algorithm (CWE-328) to store the database password. You need to recover the old password, implement a secure rotation, and generate a new configuration file.

The system contains the following files:
- `/home/user/old_config.json`: Contains the legacy credential configuration, including the weak password hash.
- `/home/user/wordlist.txt`: A dictionary of commonly used passwords in your organization.

Perform the following steps:
1. **Analyze and Crack:** Inspect `/home/user/old_config.json` to identify the weak hashing algorithm used. Write a Python script to crack the hash using `/home/user/wordlist.txt` to recover the plaintext password.
2. **File Integrity Verification:** Calculate the SHA256 checksum of `/home/user/wordlist.txt` to ensure the integrity of the source dictionary.
3. **Secure Credential Rotation:** Create a Python script `/home/user/rotate.py` that generates a new secure configuration. The new configuration must use a 16-byte cryptographically secure random salt (hex-encoded to 32 characters) and use SHA256 to hash the recovered password. The hash should be computed over the string concatenation of the hex salt and the plaintext password (i.e., `sha256(salt + password)`).
4. **Output Generation:** Your script must write the new configuration to `/home/user/new_config.json` with the following exact JSON structure:

```json
{
  "service": "db",
  "recovered_password_length": <integer_length_of_cracked_password>,
  "new_hash_algorithm": "sha256",
  "salt": "<32_character_hex_string>",
  "password_hash": "<64_character_hex_string_of_sha256(salt+password)>",
  "wordlist_checksum": "<64_character_hex_string_of_wordlist_sha256>"
}
```

Ensure `/home/user/new_config.json` is formatted as valid JSON. Do not modify or delete the original files.
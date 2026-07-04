You are a DevSecOps engineer at a company migrating to a new "Policy as Code" framework. 

An internal legacy web service provisions SSH access by generating custom session tokens. These tokens are verified by a legacy compiled daemon. We have discovered multiple security issues with how these tokens were historically generated: some tokens embed deprecated SSH key types, and some embed weak password hashes that are vulnerable to brute-force attacks.

Your task is to write a Python script, `/home/user/filter.py`, that acts as a strict security pre-filter for these tokens. Your script must read a single token string from standard input (`stdin`) and exit with status code `0` if the token is completely secure and valid, or exit with status code `1` if it is invalid or violates our new security policies.

**System Context & Requirements:**
1. **The Oracle Daemon:** A legacy, stripped binary is running in the background on your system. It is bound to a random local TCP port between `8000` and `9000`. You can send a raw token string (followed by a newline) to this daemon over TCP, and it will respond with either `VALID\n` or `INVALID\n` and then close the connection. Your script must use this daemon to verify the cryptographic signature of the token.
2. **Token Format:** The tokens are Base64-encoded strings. When decoded, they are pipe-separated (`|`) strings with the following structure:
   `username|ssh_public_key|sha256_password_hash|signature`
3. **SSH Hardening Policy:** The embedded `ssh_public_key` string MUST strictly begin with either `ssh-ed25519` or `ecdsa-sha2-nistp256`. Any other key types (such as `ssh-rsa` or `ssh-dss`) are insecure and must be rejected.
4. **Anti-Brute-Force Policy:** The `sha256_password_hash` is a standard SHA-256 hex digest of the user's password. You are provided a dictionary of banned, weak passwords at `/home/user/wordlist.txt`. Your script must attempt to crack the hash using this wordlist. If the hash matches any password in the wordlist, the token must be rejected.

**Success Criteria:**
We have placed two datasets on your machine:
- `/home/user/corpus/clean/`: Contains tokens that are perfectly valid, use secure SSH keys, and have strong passwords.
- `/home/user/corpus/evil/`: Contains tokens that fail one or more of the checks (invalid signatures, weak SSH keys, or crackable passwords).

Your script `/home/user/filter.py` must reliably evaluate any token piped to it. An automated test will pipe every file in the `clean` and `evil` directories to your script. To pass, your script must exit `0` for 100% of the clean tokens and exit `1` for 100% of the evil tokens.
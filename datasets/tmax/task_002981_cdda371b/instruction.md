We are in the process of deprecating a legacy authentication service because it has a severe security flaw: it accepts credentials via command-line arguments, which exposes them to anyone observing `/proc`. 

The legacy token generator is a compiled Linux binary located at `/app/legacy_auth`. It takes a username and password as arguments and outputs an authentication token. We need to implement this exact same token generation logic in Python so we can integrate it securely into our new backend without leaking credentials to process lists.

Your task is to:
1. Analyze the stripped binary `/app/legacy_auth` to figure out the cryptographic operations it performs. (Hint: It uses a standard encryption algorithm, some padding, and a hardcoded secret key).
2. Write a Python script at `/home/user/secure_auth.py` that implements the exact same logic.
3. The script must accept two arguments (username and password) and print the resulting token to standard output, exactly matching the format of the legacy binary.

Example of the legacy binary usage:
`/app/legacy_auth admin MySecretPassword123`
Output: `TOKEN: <some_base64_or_hex_string>`

Requirements for `/home/user/secure_auth.py`:
- It must take exactly two command-line arguments: username and password.
- It must print ONLY the token output in the exact same format as the binary.
- It must perfectly replicate the cryptographic logic, including any secrets or keys used by the binary.

The automated verification will run a test suite against your script, passing 100 random username/password pairs and comparing the output against the legacy binary. You must achieve a 100% match rate.
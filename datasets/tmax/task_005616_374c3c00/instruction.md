You are performing a local penetration test on a machine. You have discovered a directory `/home/user/vault/` containing a custom authentication script `service.py` and a hex-encoded file `low_priv.hex`.

The `service.py` script is used to generate and validate access tokens for a local privilege management service. Analyzing the script, you notice that the encryption key is derived from a weak 4-digit PIN (0000-9999). 

The `low_priv.hex` file contains the hex-encoded ciphertext of a valid token for the "guest" user. The original unencrypted token payload for this user is exactly: `{"user": "guest", "role": "guest"}`.

Your task:
1. Write a Python script to brute-force the 4-digit PIN by attempting to decrypt the contents of `low_priv.hex` until it matches the known guest payload.
2. Once you have the PIN, generate a new encrypted token for the admin user. The payload must be exactly: `{"user": "admin", "role": "root"}`.
3. Save the resulting encrypted admin token as a **hex-encoded string** to the file `/home/user/admin_token.txt`. 

Note: You may need to install the `pycryptodome` library (`pip install pycryptodome`) if it is not already installed.
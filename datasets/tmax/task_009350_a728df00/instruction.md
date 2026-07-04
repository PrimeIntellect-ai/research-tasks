You are a penetration tester performing a vulnerability assessment on a simulated internal network. During your reconnaissance, you intercepted a secure configuration payload, but it is encrypted. You have gathered some intelligence about the target's cryptographic implementation.

Your objective is to decrypt the intercepted payload, recover the hidden access parameters, and craft a forged authentication token to achieve privilege escalation.

Here is the intelligence you have:
1. The encrypted payload is saved at `/home/user/intercepted_data.bin`.
2. The payload is encrypted using AES-CBC. The initialization vector (IV) is exactly the first 16 bytes of the file.
3. The encryption key is derived by taking the SHA-256 hash of a 4-digit numeric PIN (e.g., from `"0000"` to `"9999"`). The resulting 32-byte hash is used directly as the AES-256 key.
4. The decrypted plaintext is PKCS7 padded. Once unpadded, it reveals a JSON object containing the target endpoint and the required role.

Your tasks:
1. Write a Python script to brute-force the 4-digit PIN and decrypt the payload. 
2. Save the discovered 4-digit PIN to a file named `/home/user/pin.txt`.
3. Extract the `role_required` value from the decrypted JSON payload.
4. The target application uses JSON Web Tokens (JWT) for authentication. Craft a forged JWT using the `HS256` algorithm. 
   - The JWT secret key is the exact 4-digit PIN string (e.g., `"1234"`).
   - The JWT payload must be a JSON object containing exactly two claims: `"user"` set to `"attacker"` and `"role"` set to the exact `role_required` value you extracted from the decrypted payload.
5. Save the final forged JWT string into a file named `/home/user/forged_token.txt`.

Ensure your final output files (`/home/user/pin.txt` and `/home/user/forged_token.txt`) contain strictly the requested data with no extra text or whitespace. You may install standard Python cryptography libraries such as `cryptography` and `PyJWT` using pip to assist you.
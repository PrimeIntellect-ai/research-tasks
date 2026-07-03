You are a security engineer tasked with rotating a compromised session credential. We have intercepted the HTTP logs of an attacker and stored them in `/home/user/access.log`. 

Your goal is to identify the compromised session, extract the old secret, generate a new cryptographically secure secret based on our rotation policy, and produce the new encoded session token.

Please complete the following steps:
1. Inspect the HTTP requests in `/home/user/access.log`. Find the request that contains the header `X-Action: Rotate-Target`.
2. From this specific request, extract the Base64-encoded payload from the `auth_session` cookie (format: `Cookie: auth_session=<base64_payload>`).
3. Decode the Base64 payload. It is a JSON object containing a `user` and a `secret`.
4. Generate a new secret using Python. The new secret must be the SHA-256 hash (in lowercase hex format) of the old `secret` concatenated with the exact string `"ROTATED"`.
5. Create a new JSON payload with the same `user` but the newly calculated `secret`. The JSON string must have no spaces (e.g., `{"user":"admin","secret":"<new_secret_hex>"}`).
6. Encode this new JSON string in Base64.
7. Save ONLY the final Base64 string to `/home/user/new_token.txt`.

Write a Python script at `/home/user/rotate.py` to automate the decoding, hashing, and encoding process. Run your script to generate `/home/user/new_token.txt`.
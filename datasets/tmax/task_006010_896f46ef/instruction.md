You are a network engineer performing a security audit on an internal authentication service. 

During your packet inspection, you saved a snippet of HTTP traffic to `/home/user/traffic.log`. This log contains a request made by a standard user, which includes a JSON Web Token (JWT) in the `Authorization` header.

You also obtained the authentication binary that validates these tokens, located at `/home/user/auth_checker` (an ELF executable). 

Recent vulnerability scans suggest that the JWT implementation used by this binary might be vulnerable to the `alg=none` signature bypass attack. 

Your task is to exploit this vulnerability:
1. Extract the valid JWT from `/home/user/traffic.log` to understand the standard payload structure.
2. Analyze the `/home/user/auth_checker` binary to discover the hidden administrator role name (it is a string containing `administrator`).
3. Write a Python script at `/home/user/forge.py` that crafts a forged JWT. The forged token must:
   - Use the `none` algorithm to bypass signature verification.
   - Set the `user` claim to `admin`.
   - Set the `role` claim to the hidden administrator role you discovered.
4. Run your Python script to generate the forged token and save the raw token string into `/home/user/forged.jwt`.
5. Execute `/home/user/auth_checker <contents_of_forged.jwt>`. If successful, the binary will output a flag. Save this flag to `/home/user/flag.txt`.

Ensure your base64url encoding is correct (no padding, correct character replacements) as expected by standard JWT implementations.
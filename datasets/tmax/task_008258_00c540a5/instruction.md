You are a security auditor checking the permissions and authentication mechanisms of an internal web service. 

We have discovered an old compiled client binary located at `/home/user/auth_client`. This binary contains a hardcoded JWT (JSON Web Token) used for low-privileged guest access. 

Recent code review of the backend Python application revealed a severe vulnerability: the JWT validation library is misconfigured and accepts tokens with the algorithm set to `none` (meaning no signature verification is performed).

Your task:
1. Extract the hardcoded JWT from the `/home/user/auth_client` binary.
2. Decode the token to understand its payload structure.
3. Forge a new JWT that exploits the `alg: "none"` vulnerability. The forged token must:
   - Have the header `{"alg":"none","typ":"JWT"}`.
   - Have the same payload structure as the extracted token, but with the `role` claim changed to `"admin"`.
   - Contain NO spaces in the JSON representation before Base64Url encoding.
   - Omit the signature (but include the trailing dot, as required by the JWT standard for unpadded/unsigned tokens).
4. Write ONLY the forged JWT string to `/home/user/admin_token.txt`.

Note: Standard JWTs use Base64Url encoding without padding (`=`). You may use Python, bash, or standard command-line tools to extract and forge the token.
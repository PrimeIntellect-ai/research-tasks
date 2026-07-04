You are an incident responder investigating a recent security breach. We discovered that an attacker bypassed our authentication system because our legacy Bash-based JWT validation script was vulnerable to the `alg: none` attack (accepting tokens with no signature) and failed to securely handle Base64URL encoding edge cases.

We have disabled the old script and need you to write a secure replacement in Bash.

**Stage 1: Recover the Secret**
The attacker left behind a screenshot of an internal wiki page containing the application's JWT Secret Key. This image is located at `/app/evidence.png`. You will need to extract the text from this image (e.g., using `tesseract`) to find the secret key. The format in the image will be `SECRET: <the_key>`.

**Stage 2: Secure Implementation**
Write a new token verification script at `/home/user/verify.sh`. The script must meet these exact requirements:
1. It must take exactly one argument: the JWT string.
2. It must split the token into its Header, Payload, and Signature components.
3. It must Base64URL-decode the Header and check the `alg` field. 
4. **Security Fix:** If the `alg` is `none` (case-insensitive) or anything other than `HS256`, the script must print `INVALID` to stdout and exit with status 1.
5. If the algorithm is `HS256`, it must verify the signature using HMAC-SHA256 and the secret key you recovered from the image. Remember to handle Base64URL encoding (which replaces `+` with `-`, `/` with `_`, and strips `=` padding).
6. If the signature is correct, print `VALID` to stdout and exit with status 0. If incorrect, print `INVALID` and exit with status 1.
7. For any malformed input (not 3 parts, bad base64, etc.), print `INVALID` and exit with status 1.

Your implementation will be exhaustively tested against a secure reference binary via random fuzzing to ensure it handles all edge cases, bypass attempts, and formatting anomalies in a bit-exact equivalent manner.

Ensure the script is executable (`chmod +x /home/user/verify.sh`).
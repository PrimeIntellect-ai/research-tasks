You are a penetration tester auditing a proprietary web authentication service. You have intercepted a screencast video from a developer's debugging session, located at `/app/intercept_debug.mp4`. 

Your goal is to reverse-engineer their custom authentication token scheme and build a standalone analyzer tool that perfectly mimics the backend's validation logic.

First, analyze the video. Hidden in one of the frames (within the first 5 seconds) is a terminal window showing the backend configuration, which contains two critical secrets:
1. `XOR_KEY`: A numeric integer key used for their custom cookie encryption.
2. `AUTH_PREFIX`: A specific string prefix required for all valid decrypted sessions.

Next, implement the analyzer. Create an executable Python script at `/home/user/auth_analyzer.py` that takes exactly one command-line argument: a hex-encoded raw HTTP request.

The script must perform the following operations in exact order:
1. **Hex Decoding:** Decode the input hex string into bytes. Attempt to decode the bytes as UTF-8. If it is not valid UTF-8, print exactly `ERR_DECODE` to stdout and exit with code 0.
2. **HTTP Header Inspection:** Parse the HTTP headers (assume lines are delimited by `\r\n`). Look for the `Cookie` header (specifically extract the value of the `session=` cookie) and the `X-Cert-Chain` header. If either header is completely missing or the `session=` cookie is not present, print exactly `ERR_MISSING` and exit.
3. **Certificate Chain Validation:** Check the value of the `X-Cert-Chain` header. For this environment, a valid certificate chain MUST contain the substring `CN=Admin` and its MD5 hash (represented as a 32-character hex string) must end with `f`. If it fails either condition, print exactly `ERR_CERT` and exit.
4. **Cryptanalysis & Decryption:** The `session` cookie is base64-encoded. Decode it into bytes. If base64 decoding fails, print `ERR_B64` and exit. Decrypt the bytes by applying a bitwise XOR to each byte using the `XOR_KEY` discovered in the video.
5. **Validation:** Convert the decrypted bytes to a UTF-8 string (if it fails, print `ERR_AUTH`). If the resulting string starts with the `AUTH_PREFIX` discovered in the video, print exactly `SUCCESS:<decrypted_string>`. Otherwise, print exactly `ERR_AUTH`.

Ensure your script is executable (`chmod +x /home/user/auth_analyzer.py`) and perfectly handles edge cases. We will verify your script against an automated testing oracle using fuzz-equivalence.
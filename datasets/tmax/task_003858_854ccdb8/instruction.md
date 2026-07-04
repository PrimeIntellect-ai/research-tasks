You are a network engineer inspecting API traffic for a security breach. A recent vulnerability advisory warned that some endpoints might be accepting JSON Web Tokens (JWTs) with the algorithm explicitly set to "none" (unsecured JWTs), allowing attackers to bypass signature verification.

You have been provided with an HTTP access log file located at `/home/user/api_traffic.log`. Your task is to analyze this log file using a Bash script or shell commands and perform the following steps:

1. **Extract JWTs:** Parse the log to extract all JWTs passed in the `Authorization: Bearer <token>` headers.
2. **Payload Decoding & Pattern Matching:** Base64url-decode the header of each JWT. Identify the tokens where the algorithm (`alg`) is set to `none` (the match should be case-insensitive, e.g., `none`, `None`, `NONE`).
3. **Extract Subjects:** For the identified vulnerable tokens, base64url-decode the payload and extract the value of the `sub` (subject) claim.
4. **Data Consolidation:** Collect all unique compromised subjects, sort them alphabetically, and save them to a temporary file `/home/user/compromised.txt`. Each subject should be on a new line.
5. **Encryption:** Encrypt the `/home/user/compromised.txt` file using AES-256-CBC via `openssl enc` to safely store the compromised accounts. Use the password `NetSec2023`. The output file must be named `/home/user/compromised.enc`. (Note: Make sure to use pbkdf2 if required by your openssl version, e.g., `-pbkdf2`).
6. **File Permission & Cleanup:** Set the file permissions of `/home/user/compromised.enc` to strictly `600` (read and write for the owner only). Finally, securely delete or remove the plaintext `/home/user/compromised.txt` file.

Complete the task using only standard CLI tools available in a standard Linux environment (like `grep`, `awk`, `jq`, `openssl`, `base64`, etc.). Ensure the final `.enc` file has the exact required permissions and the plaintext file is removed.
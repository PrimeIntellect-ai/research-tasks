You are a DevSecOps engineer tasked with enforcing "policy as code" for a new file upload microservice. The development team has historically struggled with path traversal vulnerabilities and broken authentication. To solve this, you must write a secure, standalone gateway program in C that pre-processes uploads, validates custom authentication tokens, decodes payloads, and strictly enforces file path policies.

Your objective is to create a C program located at `/home/user/upload_gateway.c` and compile it to an executable at `/home/user/upload_gateway`.

The executable must accept exactly three command-line arguments:
`./upload_gateway <auth_token> <hex_encoded_filename> <hex_encoded_payload>`

Here are the strict requirements for each phase of the program:

### 1. Token Validation (Authentication)
The `<auth_token>` is formatted as `user_id:timestamp:signature`.
To validate the token, your program must re-calculate the signature and compare it.
The signature algorithm is:
1. Calculate the sum of the ASCII values of all characters in the `user_id`.
2. Calculate the sum of the ASCII values of all characters in the `timestamp`.
3. Add these two sums together.
4. Take the modulo 256 of the total sum.
5. Format the result as a two-character uppercase Hexadecimal string (e.g., `3A`, `0F`).

If the provided signature does not perfectly match the calculated signature, the program must:
- Append the exact string `[AUTH_FAIL] Invalid token for user: <user_id>\n` to `/home/user/audit.log`.
- Exit with status code 1.

### 2. Payload Decoding
The filename and the file payload are provided as continuous Hexadecimal strings (e.g., `68656c6c6f2e747874` for `hello.txt`).
Your program must decode both the filename and the payload from Hex into raw bytes/characters. If the hex strings have an odd length or contain invalid hex characters, exit with status code 2 and log `[DECODE_FAIL] Invalid hex input\n` to `/home/user/audit.log`.

### 3. Policy Enforcement (Path Traversal Protection)
To prevent path traversal, inspect the decoded filename. The upload must be rejected if the decoded filename contains:
- The substring `..` (two consecutive dots)
- The forward slash character `/`
- The backward slash character `\`

If any of these are detected in the decoded filename, the program must:
- Append the exact string `[POLICY_FAIL] Path traversal attempt by user: <user_id>\n` to `/home/user/audit.log`.
- Exit with status code 3.

### 4. File Writing
If all validations pass:
- Save the decoded raw payload bytes into a new file located at `/home/user/uploads/<decoded_filename>`.
- Append the exact string `[SUCCESS] File <decoded_filename> saved for user: <user_id>\n` to `/home/user/audit.log`.
- Exit with status code 0.

**Additional Setup Constraints:**
- Create the directory `/home/user/uploads/` if it does not already exist.
- Create `/home/user/audit.log` if it does not exist, or append to it if it does.
- You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.). No external libraries requiring `apt-get` installation are permitted.
- Ensure your compiled binary is executable.

Test your binary thoroughly using the shell to ensure all logic (token parsing, hex decoding, path traversal prevention) works accurately before completing the task.
You are a DevSecOps engineer tasked with implementing a Policy-as-Code execution engine. To prevent unauthorized or malicious deployment scripts from running in our CI/CD pipeline, all deployment payloads are heavily obfuscated, encrypted, and require integrity verification before execution in an isolated environment.

You must create a Bash script at `/home/user/runner.sh` that processes a payload file and executes it according to strict security policies.

The script must take exactly one argument: the path to a payload data file (e.g., `/home/user/payload.dat`).

The payload file is a plain text file structured exactly as follows (one component per line):
Line 1: A 64-character hex string representing the 256-bit AES Key.
Line 2: A 32-character hex string representing the 128-bit AES IV.
Line 3: A Base64-encoded ciphertext. This was encrypted using AES-256-CBC.
Line 4: A 64-character hex string representing the expected SHA-256 checksum of the **final raw bash script**.

Your script `/home/user/runner.sh` must perform the following actions:
1. **Decryption**: Decrypt the ciphertext from Line 3 using the Key and IV provided in Lines 1 and 2. The cipher used is `aes-256-cbc`.
2. **Decoding**: The decrypted plaintext is itself a Base64-encoded string. Base64-decode this plaintext to reveal the raw Bash script.
3. **Verification**: Compute the SHA-256 checksum of the decoded raw Bash script. Compare it exactly against the expected checksum on Line 4.
4. **Enforcement & Execution**:
   - If the checksum does NOT match, the script must immediately write exactly the string `POLICY_VIOLATION: CHECKSUM_MISMATCH` to `/home/user/execution.log` and exit with status code 1.
   - If the checksum matches, execute the raw Bash script in a restricted environment:
     - The script must be executed with a completely empty environment (no environment variables passed down).
     - The script must be subject to a strict timeout of 5 seconds.
   - Capture the standard output of the successfully executed payload and write it to `/home/user/execution.log`.

Make sure `/home/user/runner.sh` is executable. 

For testing purposes, a file `/home/user/payload.dat` has been placed in your environment. Run your script against this file to generate the final `/home/user/execution.log` which will be verified by our automated systems.
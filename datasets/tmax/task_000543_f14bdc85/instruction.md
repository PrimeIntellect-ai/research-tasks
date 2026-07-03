You are a DevSecOps engineer implementing "policy as code" for a new logging pipeline. A developer has submitted a custom encryption utility for securing sensitive logs, but it has not been vetted. 

Your objective is to write and execute a Bash script at `/home/user/enforce.sh` that processes a raw log file, safely executes the untrusted encryption utility using process isolation, and performs a basic differential cryptanalysis check to prove the utility's weakness.

Here are the exact requirements for your script:

1. **Sensitive Data Redaction**: 
   Read the file `/home/user/raw.log`. Use standard command-line tools (e.g., `sed` or `awk`) to redact all IPv4 addresses in the text, replacing them exactly with the string `[REDACTED]`.

2. **Process Isolation**: 
   The untrusted encryption tool is located at `/home/user/encrypt.py`. It reads plaintext from standard input and prints a hexadecimal ciphertext to standard output. 
   Pass your redacted log text to this script via standard input. Because the script is untrusted, you must execute it in an isolated environment:
   - Strip all environment variables (using `env -i`).
   - Run it without network access (using `unshare -n`).
   Save the final encrypted hex output to `/home/user/encrypted.log`.

3. **Differential Cryptanalysis**: 
   The custom encryption is suspected of being a trivially weak stream cipher, making it vulnerable to known-plaintext and differential attacks. To demonstrate this, you must analyze how the ciphertext changes given a single-byte difference in plaintext.
   - Encrypt the exact string `BLOCK_A` using the same isolated execution of `/home/user/encrypt.py`.
   - Encrypt the exact string `BLOCK_B` using the same isolated execution.
   - Calculate the bitwise XOR of the two resulting hex-encoded ciphertexts.
   - Save the resulting XOR difference as a continuous lowercase hexadecimal string (with leading zeros preserved, no `0x` prefix) to `/home/user/diff_analysis.txt`.

Ensure your script is executable and run it so the output files (`/home/user/encrypted.log` and `/home/user/diff_analysis.txt`) are generated.
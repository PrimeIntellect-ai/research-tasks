You are a penetration tester performing a security audit on a simulated web backend environment. 

During your enumeration, you discovered that a custom C-based web daemon periodically spawns a helper process to handle authentication. It appears this daemon is vulnerable to an information disclosure flaw: it passes encrypted credentials to the helper process via command-line arguments, which briefly become visible in `/proc/cmdline`. 

The system administrators have set up a process monitoring script that logs snapshots of these command lines to a log file. You have managed to download the source code of the vulnerable web daemon and the process monitoring logs.

Your objective is to:
1. Analyze the web daemon's source code at `/home/user/service.c` to understand the custom encryption algorithm and identify the hardcoded encryption key.
2. Parse the process monitor log at `/home/user/process_snaps.log` to find the leaked ciphertext of the administrator's authentication token.
3. Write a C program at `/home/user/decrypt.c` that implements the decryption routine. Compile and execute it to recover the plaintext authentication token.
4. Save the exact recovered plaintext token to `/home/user/recovered_token.txt` (ensure there are no trailing newlines unless they are part of the token).
5. Compute the SHA256 hash of the recovered plaintext token and save the hash string to `/home/user/token_hash.txt`.

Constraints:
- Do not use root/sudo commands.
- You must write the decryption logic in C.

Information provided to you during setup (assume these already exist in the environment):
- `/home/user/service.c`: The C source file of the web daemon.
- `/home/user/process_snaps.log`: The log file containing scraped `/proc/cmdline` entries.
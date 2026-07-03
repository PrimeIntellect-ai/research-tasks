You are a network security engineer investigating a potential data breach on a compromised Linux workstation. You have discovered a suspicious script at `/home/user/exfiltrator.py` and a hex dump of a network payload it recently transmitted, saved at `/home/user/exfil.hex`. 

Your investigation indicates that the script exfiltrated a sensitive SSH private key by encrypting it with a repeating-key XOR cipher.

Perform the following steps to analyze the breach and secure the system:

1. **Cryptanalysis & Decryption:**
   The file `/home/user/exfil.hex` contains the hex string of the encrypted SSH private key. 
   Since it is a standard OpenSSH private key, you know it begins with the plaintext `-----BEGIN OPENSSH PRIVATE KEY-----`.
   Use this known plaintext to recover the repeating XOR key. Write a script in a language of your choice (e.g., Python, C, Bash) to decrypt the entire hex dump.
   Save the fully decrypted SSH private key to `/home/user/recovered_id_rsa` and ensure it has the correct standard file permissions for an SSH private key.

2. **Process Isolation / Sandboxing:**
   You must safely execute the malware to observe its output, but you must prevent it from making any network connections. 
   Use `bwrap` (Bubblewrap) to run `/home/user/exfiltrator.py` with the recovered XOR key as its single command-line argument. 
   Configure the `bwrap` sandbox with the following strict constraints:
   - Provide read-only access to the entire host filesystem (`/`).
   - Create a fresh, empty `tmpfs` mounted at `/tmp`.
   - Disable network access entirely for the sandbox (unshare the network namespace).
   Redirect the standard output of this sandboxed execution to `/home/user/isolated_run.log`.

3. **SSH Hardening:**
   To prevent the attacker from using the compromised key while maintaining it for forensics, generate the corresponding public key for `/home/user/recovered_id_rsa`.
   Create a file named `/home/user/hardened_authorized_keys` containing this public key, but prepend the following security options to the public key line to restrict its capabilities:
   `no-pty,no-port-forwarding,command="/bin/false"`

Ensure all output files (`recovered_id_rsa`, `isolated_run.log`, `hardened_authorized_keys`) are precisely generated and placed in `/home/user/`.
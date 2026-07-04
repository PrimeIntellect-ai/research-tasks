You are a security engineer tasked with rotating compromised SSH credentials on a critical jump server. The previous administrator left an encrypted backup of the deployment scripts, but the password was written on a physical sticky note. 

Your multi-stage task is as follows:

1. **Information Extraction & Decryption:**
   There is an image of the sticky note located at `/app/sticky_note.png`. Extract the text from this image. Use this text as the passphrase to decrypt the file `/home/user/ssh_backup.enc`. The file was encrypted using `openssl enc -aes-256-cbc -pbkdf2`. Output the decrypted archive to `/home/user/ssh_backup.tar.gz` and extract it into `/home/user/backup/`.

2. **Privilege Escalation Auditing:**
   Inside the extracted backup, you will find a Python script named `deploy_keys.py`. This script is intended to be run with elevated privileges via sudo to copy SSH keys into a restricted system directory. However, it contains a privilege escalation vulnerability related to how it executes system commands. Audit and fix this Python script so that it securely copies files without allowing arbitrary command injection. Overwrite the fixed script at `/home/user/backup/deploy_keys.py`.

3. **Algorithmic Key Generation:**
   For compliance reasons, our new SSH keys must meet a strict "vanity fingerprint" requirement to prevent spoofing. Write a Python script to algorithmically generate new Ed25519 SSH keypairs until you find one where the SHA256 hex digest of the *base64 encoded public key string* (excluding the "ssh-ed25519 " prefix and any trailing comments/newlines) starts with at least five leading zeros (e.g., `00000...`). 
   Save the winning private key to `/home/user/new_key` and the public key to `/home/user/new_key.pub`. Ensure both files have the correct, hardened filesystem permissions for SSH keys.

4. **Integration:**
   Run your fixed `/home/user/backup/deploy_keys.py` to deploy `/home/user/new_key.pub` to the target directory specified in the script.

Ensure all final key files are placed exactly at `/home/user/new_key` and `/home/user/new_key.pub`, and that your modified deployment script is at `/home/user/backup/deploy_keys.py`.
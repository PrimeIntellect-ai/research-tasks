You are a network engineer tasked with troubleshooting and securing a zero-trust SSH bastion environment. The environment consists of a restricted internal API and a user-space SSH daemon used for port forwarding. Recently, unauthorized keys have been attempting to bypass access controls, and you need to implement a strict key auditing script, configure the SSH bastion, and restore connectivity to the internal API.

Your objectives are as follows:

1. **Backup Existing Configuration:**
   The current SSH configuration is located at `/home/user/bastion/sshd_config`. Before making any changes, securely back up this file to `/home/user/backup/sshd_config.bak`.

2. **Develop an SSH Key Auditor (Adversarial Corpus Verification):**
   You must write a Python script at `/home/user/key_auditor.py` that analyzes a single OpenSSH public key file.
   The script must take the file path as its first command-line argument: `python3 /home/user/key_auditor.py <path_to_pubkey>`
   
   The script must exit with status `0` (clean) if the key passes ALL the following security rules, and exit with status `1` (evil) if it violates ANY rule:
   - Reject any RSA keys that are less than 2048 bits (you may parse the key data or use standard CLI tools like `ssh-keygen -l -f`).
   - Reject any key that includes a forced command option (i.e., the string `command=` anywhere in the key options).
   - Reject any key where the comment field (the third space-separated field in a standard key, if present) contains the exact substring `admin`.
   - Accept valid `ssh-ed25519`, `ecdsa-sha2-nistp256`, and valid `ssh-rsa` (>= 2048 bits) keys that do not violate the above rules.
   
   *Note: Your script will be tested against a hidden corpus of clean and evil keys to verify its accuracy. It must reject 100% of the evil corpus and preserve/accept 100% of the clean corpus.*

3. **Service Orchestration & Process Monitoring:**
   There are two services you must configure and start:
   - An internal Flask API located at `/app/api.py`. Start this service in the background. It binds to `127.0.0.1:5000`.
   - A user-space SSH daemon. Generate a host key (`/home/user/bastion/ssh_host_ed25519_key`) and an SSH keypair for yourself (`/home/user/.ssh/id_ed25519`). Ensure your newly generated public key passes your `key_auditor.py` script. Add your valid public key to `/home/user/.ssh/authorized_keys`.
   Modify `/home/user/bastion/sshd_config` to ensure it listens on port `2222`, uses your newly generated host key, and has `StrictModes no` and `UsePAM no` to run successfully without root privileges. Start the SSH daemon in the background using `sshd -f /home/user/bastion/sshd_config`.

4. **SSH Tunneling & Integration:**
   Using your newly created SSH key, establish a local port forward through the bastion (port 2222) to expose the internal Flask API. Forward your local port `8080` to `127.0.0.1:5000` through the bastion.
   
   Once the tunnel is established, verify connectivity by running:
   `curl -s http://127.0.0.1:8080/status > /home/user/api_status.log`

Ensure all services remain running in the background and that `/home/user/api_status.log` contains the successful JSON response from the API.
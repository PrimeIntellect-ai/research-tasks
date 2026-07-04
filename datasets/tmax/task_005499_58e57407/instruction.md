You are a network engineer who recently intercepted traffic related to a custom authentication service on a compromised host. You managed to extract the authentication daemon binary. Your goal is to reverse engineer the token generation process, validate the intercepted traffic, and prepare a hardened SSH configuration to secure the host.

Perform the following tasks:
1. **Reverse Engineering**: Analyze the ELF binary located at `/home/user/auth_daemon` to extract the hardcoded secret key used for token generation. 
2. **Token Validation**: The authentication tokens are generated using an HMAC-SHA256 hash. The message is the timestamp (as a string), and the key is the hardcoded secret you extracted from the binary. 
   - You have been provided with an intercepted traffic log at `/home/user/intercepted.log`. Each line contains a comma-separated timestamp and token (e.g., `1600000000,abcdef123456...`).
   - Write a Python script at `/home/user/validate.py` that reads `/home/user/intercepted.log`, verifies each token, and writes the *entire line* of every valid entry to a new file at `/home/user/valid_traffic.log`.
3. **SSH Hardening**: To prevent further unauthorized access, create an SSH configuration snippet at `/home/user/sshd_config.custom`. The file must explicitly contain the following configurations (one per line, exact spelling):
   - `PermitRootLogin no`
   - `PasswordAuthentication no`
   - `Protocol 2`

Ensure that your Python script handles file reading and writing correctly, and that the SSH config file strictly follows the requested format.
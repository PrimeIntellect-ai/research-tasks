You are an incident responder investigating a compromised system. The system runs a multi-service stack consisting of an API Gateway (Nginx), a backend authentication API (Flask), and an internal SSH bastion process used for backend jobs. 

During your investigation, you discovered two major security flaws:
1. **Credential Leakage in `/proc`**: The Flask application (`/app/backend/flask_app.py`) triggers a local script (`/app/backend/helper.py`) via `subprocess.Popen`, passing plain-text credentials as command-line arguments to authenticate against the local SSHD service. This makes the credentials visible to any user on the system via `/proc`.
2. **Lack of Ingress Filtering**: The system is processing maliciously encoded payloads containing shell metacharacters and path traversals.

The environment relies on a startup script `/app/start_services.sh` which brings up Nginx (port 8080), Flask (port 5000), and a local SSHD instance (port 2222). 

Your task is to remediate the system and write an Intrusion Detection System (IDS) filter.

**Objective 1: Reconfigure and Harden the Multi-Service Stack**
1. Stop the running services, if any.
2. Generate an SSH keypair without a passphrase in `/home/user/.ssh/id_rsa`.
3. Harden the local SSH daemon configuration at `/app/sshd/sshd_config`. It must run on port 2222, explicitly disable `PasswordAuthentication`, enable `PubkeyAuthentication`, and use `/app/sshd/authorized_keys` for authorization.
4. Set up the public key in `/app/sshd/authorized_keys` with the correct permissions.
5. Modify `/app/backend/flask_app.py` and `/app/backend/helper.py` to completely remove password usage. The helper script must authenticate to the local SSHD using the newly generated SSH private key instead of a password.
6. Verify that running `/app/start_services.sh` successfully brings up all services, and `curl -s http://localhost:8080/trigger` returns `{"status": "success"}`.

**Objective 2: Build the IDS Filter**
Write a Python script at `/home/user/ids_filter.py` that classifies API payloads.
- The script must accept two arguments: an input directory path and an output CSV file path.
  Example: `python3 /home/user/ids_filter.py /home/user/corpora/test_set /home/user/results.csv`
- The input directory contains `.txt` files. Each file contains a Base64-encoded JSON string.
- Your script must read each file, decode the Base64, and parse the JSON.
- Examine the `username` and `command` fields. If either field contains any of the following shell metacharacters: `[ ; & | $ \` < > ]` or the path traversal string `../`, the payload is malicious.
- The script must output a CSV file with the exact header `filename,label`. The label must be either `clean` or `evil`. 

Your solution will be tested against hidden adversarial corpora. You must correctly classify 100% of both clean and malicious payloads, and your end-to-end API configuration must function correctly using only SSH keys.
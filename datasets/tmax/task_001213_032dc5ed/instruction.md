You are managing a local simulated microservice architecture. A startup script `/home/user/app/start_services.sh` brings up three interacting components, but the system is currently broken due to IPC permission issues, missing directory structures, and an uninitialized backend. Additionally, the API gateway needs a request sanitizer written in Bash to drop malicious payloads.

Your objectives are to fix the multi-service setup and implement the security filter:

1. **Service Reconfiguration & Gluing (Multi-Service setup):**
   - The system consists of an `api_gateway.py` (TCP port 8080), an `app_backend.py` (reads from named pipe), and a `db_service.py` (reads from named pipe).
   - Currently, the backend processes fail to communicate because the named pipes they use lack the correct symlinks and permissions.
   - Create the directory structure: `/home/user/app/ipc/v1/` and `/home/user/app/ipc/v2/`.
   - Create named pipes (FIFOs) named `backend.fifo` and `db.fifo` in `/home/user/app/ipc/v2/`.
   - Create symlinks in `/home/user/app/ipc/v1/` pointing to the `v2` FIFOs.
   - Set permissions on `/home/user/app/ipc/v2/` and the FIFOs so that only the owner (you) has read/write access (mode `0600` for files, `0700` for dirs).
   - The `db_service.py` requires interactive initialization upon startup. It prompts: `Enter DB Admin PIN:` and expects `8675309`, then it prompts `Confirm PIN:` and expects the same. Write an `expect` script at `/home/user/app/init_db.exp` that automates this interactive setup for the DB service CLI (`python3 /home/user/app/db_init_cli.py`).

2. **Adversarial Request Sanitizer:**
   - Write a Bash script at `/home/user/app/sanitizer.sh` that takes a single file path as an argument.
   - The script must read the contents of the file (representing an HTTP request payload) and print `ACCEPT` to stdout if the payload is safe, or `REJECT` if it is malicious.
   - A malicious payload is defined as containing any of the following substrings (case-insensitive): `<script>`, `DROP TABLE`, `UNION SELECT`, or `passwd`.
   - Your script will be tested against two directories of corpus files: `/home/user/corpus/clean/` and `/home/user/corpus/evil/`. 

Once you have created the directory structure, fixed the symlinks/permissions, written the `init_db.exp` script, and written the `sanitizer.sh` script, run `/home/user/app/start_services.sh` to verify everything connects. 

When you are done, output a summary log to `/home/user/app/completion.log` containing exactly two lines:
Line 1: The absolute path to the sanitizer script.
Line 2: The absolute path to the initialized database FIFO symlink.
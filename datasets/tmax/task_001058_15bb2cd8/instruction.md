You are a container specialist managing a rootless microservice deployment. The microservice requires a specific user and group configuration bind-mounted as a mock `passwd` file.

Your task is to create a robust, idempotent deployment script `/home/user/init_service.sh` and execute the steps below.

**Requirements for `/home/user/init_service.sh`:**
1. **Directory Setup**: It must ensure that `/home/user/service_data` and `/home/user/backup` directories exist.
2. **Backup Strategy**: It must check if the file `/home/user/service_data/passwd` exists. If it does, safely copy it to `/home/user/backup/passwd.bak` before making any changes. 
3. **Idempotent User Administration**: It must configure the mock user file at `/home/user/service_data/passwd`. 
   - Add a user entry exactly matching: `appuser:x:2001:2001:Microservice Account:/home/user/service_data:/bin/false`
   - This addition must be idempotent. If `appuser` already exists in the file, do not add a duplicate line or alter existing lines. If the file does not exist, create it.
4. **Robust Script Writing**: The script must generate a Python verification script at `/home/user/service_data/verify.py`. The Python script must:
   - Read `/home/user/service_data/passwd`.
   - Parse the file to find the user `appuser`.
   - Print `UID: <uid_value>` (e.g., `UID: 2001`).
   - Include robust error handling: if the file does not exist, it must catch the exception (e.g., `FileNotFoundError`) and print exactly `Error: passwd file missing`.

**Execution:**
Once you have written `/home/user/init_service.sh`:
1. Make it executable and run it.
2. Run the generated Python script and redirect its output to a log file:
   `python3 /home/user/service_data/verify.py > /home/user/result.log`

Ensure all paths are absolute and exactly as specified.
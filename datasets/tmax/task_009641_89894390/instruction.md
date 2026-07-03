I need you to help me automate our service provisioning infrastructure using a Git-driven workflow.

Please perform the following steps:

1. Initialize a new local Git repository at `/home/user/infra-repo`. (Configure standard Git user name and email so commits can be made).
2. Write a Python script at `/home/user/provisioner.py` that acts as a simple process supervisor. It must read a file located at `/home/user/requests.txt`. 
   Each line in `/home/user/requests.txt` will follow the exact format: `<ACTION> <service_name>`.
   The supported actions are `START`, `STOP`, and `RESTART`.
   For each line processed, the script should:
   - Ensure the directory `/home/user/services/<service_name>/` exists (create it if it doesn't).
   - If the ACTION is `START`, write the string `active` to `/home/user/services/<service_name>/status`.
   - If the ACTION is `STOP`, write the string `inactive` to `/home/user/services/<service_name>/status`.
   - If the ACTION is `RESTART`, write the string `restarted` to `/home/user/services/<service_name>/status`.
   The script must process all lines in the file from top to bottom, applying the status updates in order. If a file or directory does not exist yet, the script must create it.
3. Create a `post-commit` hook in the Git repository at `/home/user/infra-repo/.git/hooks/post-commit`. This hook must be executable and must run `python3 /home/user/provisioner.py` whenever a commit is made.
4. Create the empty file `/home/user/requests.txt` to avoid file-not-found errors on the first run.

Make sure all permissions are set correctly so the Git hook executes successfully when a commit is made.
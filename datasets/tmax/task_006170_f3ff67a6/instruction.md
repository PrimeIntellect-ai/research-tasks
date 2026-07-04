You are a Linux Systems Engineer tasked with automating the hardening and lifecycle management of a mock containerized service using Python.

An interactive shell tool exists at `/home/user/bin/provisioner.sh` that provisions and stops minimal mock "containers". Because it was designed for manual use, it prompts interactively for hardening configurations (storage quotas and security flags). 

Your objective is to write a Python script at `/home/user/harden_manager.py` that fully automates this lifecycle. You must use the Python `pexpect` module to handle the interactive prompts.

Your script must perform the following actions:
1. **Determine Storage Quota:** Read the maximum allowed storage limit from `/home/user/config/limits.json` (under the key `"max_storage_mb"`).
2. **Provision the Container:** Launch `/home/user/bin/provisioner.sh` using `pexpect` and answer its interactive prompts exactly as follows:
    * Prompt: `Enter container name:` -> Provide `secure-con-01`
    * Prompt: `Enter storage limit (MB):` -> Provide the exact integer value you read from the limits file.
    * Prompt: `Enable read-only rootfs? (y/n):` -> Provide `y`
3. **Capture the ID:** When the provisioner finishes, it will output a success message like: `Successfully started container [ID: <uuid>]`. Extract this container ID.
4. **Verify Storage and Lifecycle:** The provisioner simulates a running container by creating a PID file at `/home/user/run/containers/<uuid>.pid`. Your script must check that this file exists.
5. **Teardown:** Stop the container by executing `/home/user/bin/provisioner.sh --stop <uuid>` using `subprocess` or `pexpect`.
6. **Report Generation:** Create a JSON formatted report at `/home/user/hardening_report.json` containing exactly these keys and the respective captured/computed values:
    * `"container_name"`: The name you assigned ("secure-con-01")
    * `"container_id"`: The extracted UUID string
    * `"storage_allocated"`: The integer value of the storage limit used
    * `"status"`: Must be the string `"stopped"`

Constraints:
- You must write and execute the Python script.
- Ensure all file paths are absolute.
- The output report must be valid JSON.
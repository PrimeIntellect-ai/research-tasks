You are an infrastructure engineer debugging a failed continuous deployment pipeline in an unprivileged environment. 

A custom deployment runner expects a configuration file at `/home/user/deployment.json`. Currently, the `backend` service fails to start because it attempts to connect to the `cache` service before the `cache` service has finished initializing. Furthermore, the `frontend` service needs a specific restart policy, and the deployment runner requires a specific group to be present in a local mock group file.

Your task is to write an **idempotent** Python script at `/home/user/provision.py` that automates fixing this environment. When executed, your script must:

1. **Update the Deployment Configuration:**
   Read `/home/user/deployment.json` and modify it so that:
   - The `backend` service has a `"depends_on"` key mapped to a list containing `"cache"` (i.e., `"depends_on": ["cache"]`).
   - The `frontend` service's `"restart_policy"` is updated from `"none"` to `"always"`.
   Ensure that running your script multiple times does not create duplicate entries in the lists or crash.

2. **Administer Local Mock Groups:**
   The pipeline runner checks a mock group file at `/home/user/mock_group`. Your script must ensure this file exists and contains a line exactly matching:
   `deploy_admins:x:1001:app_runner`
   This step must be idempotent. If the file already exists and contains the correct group definition, it should not append duplicate lines. If the file does not exist, it should be created.

3. **Execute the Runner:**
   After configuring the files, your Python script must execute the deployment runner via `python3 /home/user/deploy_runner.py` and redirect its standard output to `/home/user/deploy_success.log`.

Do not manually edit the files. Your solution must be entirely contained within `/home/user/provision.py`, which you should run to complete the task.
You are tasked with setting up a custom automated infrastructure-deployment pipeline for a development team using a Git hook. The pipeline manages mock filesystem mounts, simulates container lifecycles, and prepares email notifications. Since you do not have root privileges, all system configurations will be directed to user-owned files.

Please complete the following steps:

1. Create a bare Git repository at `/home/user/infra.git`.
2. Write a `post-receive` Git hook inside `/home/user/infra.git/hooks/post-receive`. The hook **must** be written entirely in Python 3 (use `#!/usr/bin/env python3`).
3. Make sure the hook is executable.

The Python `post-receive` hook must perform the following actions whenever code is pushed:
* Read the standard input provided by Git (`oldrev newrev refname`).
* Extract the contents of `deploy_config.json` from the newly pushed commit (using `git show` or similar Git commands from within Python).
* **Mount/fstab configuration (Idempotent):** Read the list of mounts from the JSON array `mounts`. Each mount is a list: `[source, destination, type]`. The hook must idempotently update `/home/user/custom.fstab`. For each mount in the JSON, append the line `<source> <destination> <type> defaults 0 0` to `/home/user/custom.fstab` ONLY IF a line starting with `<source> <destination> ` does not already exist in the file.
* **Container Lifecycle Management:** The JSON will have a key `"container_action"`. If the value is `"restart"`, the hook must read `/home/user/container_status.json`, update the `"running"` key to `true` and the `"last_deployed_commit"` key to the abbreviated 7-character hash of the new commit, and write it back.
* **Email Configuration:** The JSON will have a key `"notify_email"`. The hook must generate an email notification configuration file at `/home/user/mail_out.conf` with exactly the following format:
```
To: <notify_email>
Subject: Deployment for commit <7-character-hash>
Status: Success
```

4. To trigger and test your setup, clone the bare repository to `/home/user/infra-clone`.
5. Inside the clone, create a file named `deploy_config.json` with the following exact content:
```json
{
  "mounts": [
    ["/home/user/data", "/mnt/app_data", "ext4"],
    ["/home/user/logs", "/mnt/app_logs", "tmpfs"]
  ],
  "container_action": "restart",
  "notify_email": "sysadmin@local.domain"
}
```
6. Commit this file with the message "Initial deployment config" and push it to the `master` branch of the bare repository (`origin master`).

Note: 
- Assume `/home/user/custom.fstab` might initially be empty or missing; create it if necessary.
- Assume `/home/user/container_status.json` already exists and contains `{"running": false, "last_deployed_commit": null}`.
- Ensure your Python hook gracefully handles reading from Git and executing subprocess commands safely.
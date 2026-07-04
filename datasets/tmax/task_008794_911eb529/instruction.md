You are a container specialist managing a deployment pipeline for microservices. Your team uses a Git repository to track deployment configurations, specifically filesystem mount mappings defined in an fstab-like format.

You need to implement an automated validation pipeline to prevent insecure mounts and ensure the configuration repository is regularly backed up.

Perform the following setup exclusively using the Linux terminal and Python:

1. Initialize a bare Git repository at `/home/user/deploy.git`.
2. Create a Git `pre-receive` hook written in Python at `/home/user/deploy.git/hooks/pre-receive`. Ensure it has the correct executable permissions.
3. The `pre-receive` hook must perform the following actions for every push:
   - Read from standard input, which Git provides in the format: `<old-commit> <new-commit> <ref-name>`.
   - For each updated ref, extract the contents of the file named `mounts.fstab` from the newly pushed commit (hint: use `git cat-file` or `git show`). Ignore if the file does not exist in the commit.
   - Parse `mounts.fstab`. The file follows the standard space-or-tab-separated fstab format: `<file_system> <mount_point> <type> <options> <dump> <pass>`. Ignore empty lines and lines starting with `#`.
   - Check if any defined `<mount_point>` (the second column) is exactly `/etc`.
   - If a violation (`/etc` mount) is detected, the hook must:
     a. Send an email to `admin@local.system` from `git@local.system` via an unauthenticated SMTP server running on `127.0.0.1` port `2525`. The email Subject must be exactly `Violation` and the body must be exactly `Invalid mount`.
     b. Exit with a status code of `1` to reject the push.
   - If no violations are found, exit with status code `0`.
4. Create a backup script written in Python at `/home/user/sync.py`. This script must:
   - Completely remove `/home/user/backup.git` if it already exists.
   - Copy the entire directory tree of `/home/user/deploy.git` to `/home/user/backup.git`.
5. Schedule the backup script using the current user's crontab. Create a cron job that executes `/usr/bin/python3 /home/user/sync.py` exactly every 5 minutes.

Do not start the SMTP server yourself; assume a mock SMTP server will be running on `127.0.0.1:2525` during the automated testing phase.
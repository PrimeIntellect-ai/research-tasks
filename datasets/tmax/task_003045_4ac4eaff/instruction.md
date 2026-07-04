You are tasked with building a custom user registry backup and synchronization system using Git and C. As a site administrator managing simulated user accounts, you must ensure that whenever user account data is pushed to a central repository, it is securely backed up and deployed with precise locale and timezone logging.

Perform the following steps exactly as described:

1. **Directories**: Create the following directories in `/home/user`:
   - `/home/user/user_registry.git`
   - `/home/user/active_users`
   - `/home/user/backups`

2. **Git Server Setup**:
   - Initialize a bare Git repository at `/home/user/user_registry.git`.

3. **Post-Receive Hook (in C)**:
   - Write a C program and compile it to `/home/user/user_registry.git/hooks/post-receive`. Make sure it is executable.
   - When a push is received, the Git hook must perform these actions in order:
     a. Check out/extract the latest contents of the `master` branch into `/home/user/active_users/`. (You can invoke `git` commands via `system()` or similar, ensuring you set the correct `--work-tree` or use `git archive`).
     b. Create a tarball of the `/home/user/active_users/` directory at `/home/user/backups/latest.tar.gz`.
     c. Enforce secure access: Set the file permissions of `/home/user/backups/latest.tar.gz` to strictly `0400` (read-only for the owner, no permissions for anyone else).
     d. Configure the environment within the C program to use the `Asia/Tokyo` timezone (using the `TZ` environment variable).
     e. Append a log entry to `/home/user/sync.log`. The log format must be exactly:
        `[YYYY-MM-DD HH:MM:SS JST] Registry updated`
        (Use standard C time functions like `strftime` with `%Y-%m-%d %H:%M:%S %Z` after setting the timezone to ensure `JST` is correctly printed).

4. **Triggering the Workflow**:
   - Clone the bare repository to `/home/user/registry_clone`.
   - Inside the clone, create a file named `admin_user.conf` containing the text `role=superuser`.
   - Add, commit (on the `master` branch), and push this file to the bare repository. This push must successfully trigger your compiled C hook.

Ensure your C program robustly handles the environment configuration and system calls. Do not use root privileges (`sudo` or `su`); all operations should be performed as the default user.
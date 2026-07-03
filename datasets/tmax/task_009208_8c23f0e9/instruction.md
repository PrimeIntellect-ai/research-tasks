You are a Linux systems engineer responsible for implementing a custom user-space storage watchdog. Because we operate in an environment where standard quota systems and root access are unavailable, we need a Bash-based daemon to monitor a specific directory's size and harden configuration files if a soft quota is exceeded.

Your task is to write a Bash script, set up the environment, and perform a simulated run to prove the script works correctly.

Here are your detailed requirements:

1. **Environment Setup**:
   - Create the directory structure: `/home/user/vault/data` and `/home/user/vault/config`.
   - Create a sensitive file: `/home/user/vault/config/master.key` containing the text `SECRET_KEY_DATA`. Set its initial permissions to `0600`.

2. **The Watchdog Script (`/home/user/watchdog.sh`)**:
   - Write a bash script at `/home/user/watchdog.sh` and make it executable.
   - The script must run continuously in a loop, sleeping for 2 seconds between iterations.
   - In each iteration, it must calculate the total disk usage of `/home/user/vault/data` in kilobytes. (Use `du -sk` to get the integer value in KB).
   - **The Soft Quota**: 2048 KB (2 MB).
   - **Lockdown Condition (Usage > 2048 KB)**:
     If the usage exceeds 2048 KB, the script must perform a hardening lockdown. It should:
     - Change the permissions of `/home/user/vault/config/master.key` to `0400` (read-only for owner).
     - Append a line to `/home/user/vault/audit.log` with exactly this format: `LOCKED <UNIX_TIMESTAMP>`.
     - *Idempotency requirement*: It must NOT repeatedly log or attempt to change permissions if it is already in a locked down state. Use a state file (`/home/user/vault/.lockdown`) to track this.
   - **Restore Condition (Usage <= 2048 KB)**:
     If the usage is 2048 KB or less, and the system is currently in a lockdown state, it must:
     - Restore the permissions of `/home/user/vault/config/master.key` to `0600`.
     - Append a line to `/home/user/vault/audit.log` with exactly this format: `UNLOCKED <UNIX_TIMESTAMP>`.
     - Clear the state file so the script knows it is no longer locked down.

3. **Execution and Testing**:
   You must demonstrate that your script works by performing the following actions in the terminal:
   - Start your `/home/user/watchdog.sh` script in the background.
   - Trigger the lockdown by creating a file larger than 2MB in `/home/user/vault/data/` (e.g., using `dd`).
   - Sleep for at least 3 seconds to allow the watchdog to detect the change and write to the audit log.
   - Trigger the unlock by deleting the large file you just created.
   - Sleep for at least 3 seconds to allow the watchdog to detect the drop in size and write the unlock event to the audit log.
   - Kill the background watchdog process gracefully.

When you are finished, the automated test will verify the existence and contents of `/home/user/vault/audit.log`, verifying that exactly one `LOCKED` event and exactly one `UNLOCKED` event were recorded, in that order.
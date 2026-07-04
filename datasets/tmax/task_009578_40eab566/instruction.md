You are acting as a site administrator managing simulated user account storage configurations. Since you do not have root access, you will be setting up directory structures, symbolic links, and generating configuration files that would typically be applied to the system later.

You have been provided with a file at `/home/user/accounts.txt` containing user account information in the format: `username:department:quota_id`.

Your task is to perform the following operations:

1. **Directory and Link Management**:
   For every user listed in `/home/user/accounts.txt`:
   - Create a base directory for them at `/home/user/site_users/<username>/`
   - Inside their base directory, create two subdirectories: `workspace` and `shared_data`.
   - Create a symbolic link inside their base directory named `dept_link` that points to the pre-existing department directory at `/home/user/departments/<department>`.

2. **Idempotent fstab Scripting**:
   Write a script at `/home/user/setup_mounts.sh` (make sure it is executable). When run, this script must read `/home/user/accounts.txt` and update a mock fstab file located at `/home/user/custom_fstab`.
   - For each user, the script must ensure the following bind mount line exists in `/home/user/custom_fstab`:
     `/home/user/global_share /home/user/site_users/<username>/shared_data none bind 0 0`
   - The script must be **idempotent**. If `/home/user/setup_mounts.sh` is executed multiple times, it must not create duplicate lines in `/home/user/custom_fstab` for the users. 
   - Note: `/home/user/custom_fstab` might already contain other lines (e.g., `/dev/sda1 / ext4 defaults 1 1`). Your script must leave unrelated lines completely intact and unmodified.

3. **Reporting**:
   Use text processing tools to generate a report at `/home/user/report.txt`. The report should extract the user and department from `accounts.txt` and list them in the following exact format, sorted alphabetically by username:
   ```
   alice -> engineering
   bob -> sales
   ```

Please write your script, execute it at least once to ensure `/home/user/custom_fstab` is populated, and generate the required directory structures and the report.
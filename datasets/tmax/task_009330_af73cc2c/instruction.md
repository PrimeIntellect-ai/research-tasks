You are a cloud architect automating the migration of a legacy analytics service to a new environment. The migration process relies on an interactive C++ binary that validates system configurations before proceeding.

Your task is to write the C++ validation program, compile it, automate its interactive prompt using `expect`, and draft the appropriate filesystem mount configuration.

Perform the following steps:

1. Write a C++ program at `/home/user/migrator.cpp` with the following requirements:
   - It must check the environment variables `TZ`, `LC_ALL`, and `DATA_MOUNT`.
   - If `TZ` is not exactly `Europe/Berlin`, it must exit with status `1`.
   - If `LC_ALL` is not exactly `de_DE.UTF-8`, it must exit with status `2`.
   - If `DATA_MOUNT` is not exactly `/tmp/migration_data`, it must exit with status `3`.
   - If all environment variables are correct, it must print exactly `"Begin migration? [y/N]: "` to standard output.
   - It must read a single word from standard input.
   - If the input is exactly `"y"`, it must write the string `"MIGRATION_READY"` to a file located at `/home/user/migration_status.txt`, and then exit with status `0`.
   - If the input is anything else, it must exit with status `4`.

2. Compile the program to `/home/user/migrator` (use standard `g++ /home/user/migrator.cpp -o /home/user/migrator`).

3. Write an Expect script at `/home/user/automate.exp` that automates this program:
   - The script must properly set the `TZ`, `LC_ALL`, and `DATA_MOUNT` environment variables to the required values before spawning the process.
   - It must spawn `/home/user/migrator`.
   - It must expect the `"Begin migration? [y/N]: "` prompt.
   - It must send `"y"` (with a carriage return) to proceed.
   - It must wait for the process to finish successfully (EOF).
   - Ensure the script has executable permissions (`chmod +x /home/user/automate.exp`) and begins with the standard `#!/usr/bin/expect` shebang.

4. The analytics data will be mounted on a dedicated block device in the new cloud environment. Create a text file at `/home/user/fstab_entry.txt` containing exactly one line: the valid `/etc/fstab` entry required to mount the device `/dev/xvdf` to the mount point `/tmp/migration_data` using the `ext4` filesystem. Use the mount options `defaults,noatime` and set the dump and fsck pass values to `0` and `2`, respectively. Fields should be separated by spaces or tabs.
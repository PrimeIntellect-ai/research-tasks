You are acting as a site administrator managing user account storage allocations. Since you do not have root privileges in this environment, you are building a custom userspace toolchain to manage a simulated `fstab` configuration for user-specific data mounts.

Complete the following steps to build the automated user storage management tool:

1. **Interactive Provisioning Script**: 
   Create a bash script at `/home/user/add_user_mount.sh`. This script must be interactive. It should prompt the administrator for three exact inputs in this specific order:
   - "Username: "
   - "Mountpoint: "
   - "Filesystem: "
   
   The script must take these inputs and append a standard `fstab`-formatted line to `/home/user/custom_fstab`. The appended line must be formatted exactly as:
   `<Username> <Mountpoint> <Filesystem> defaults 0 0`
   Ensure the script is executable.

2. **Simulate Provisioning**:
   Use your script to provision storage for three new users by feeding it the following inputs (you can use standard input redirection, `expect`, or here-documents to run your interactive script):
   - User 1 -> Username: `alice`, Mountpoint: `/mnt/alice_data`, Filesystem: `ext4`
   - User 2 -> Username: `bob`, Mountpoint: `/mnt/bob_data`, Filesystem: `xfs`
   - User 3 -> Username: `charlie`, Mountpoint: `/mnt/charlie_data`, Filesystem: `ext4`

3. **C-based Fstab Parser Service**:
   Write a C program at `/home/user/fstab_parser.c`. This program will act as our configuration monitor. It must:
   - Read the `/home/user/custom_fstab` file.
   - Parse each valid line to extract the filesystem type (the third column).
   - Count the total number of mounts per filesystem type.
   - Output the summary to `/home/user/fs_summary.log` in the format `<fstype>:<count>`, with one entry per line.
   - The output must be sorted alphabetically by the filesystem type.

4. **Compilation and Execution**:
   Compile your C program into an executable named `/home/user/fstab_parser` using `gcc`. 
   Run the compiled executable to generate the final `/home/user/fs_summary.log`.

Ensure all file paths are absolute and exactly match the instructions.
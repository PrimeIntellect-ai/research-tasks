You are a system engineer diagnosing why a critical local daemon fails to start. The daemon requires a specific filesystem state to run properly. Your objective is to establish a robust environment for the daemon by creating an idempotent setup script, a C++ health monitor, a backup strategy, and an automated interactive restore script.

Please complete the following tasks:

1. **Idempotent Setup Script**:
   Write a bash script at `/home/user/setup.sh` that ensures the directory `/home/user/service_data` exists. Inside this directory, it must ensure a file named `state.dat` exists containing exactly the string `READY` (without trailing newlines, or with a single newline, both are fine as long as the word is present). The script must be idempotent: running it multiple times should not result in errors or change the state if it is already correct. Make the script executable.

2. **C++ Health Monitor**:
   Write a C++ program at `/home/user/monitor.cpp` and compile it to `/home/user/monitor`. 
   The program should read `/home/user/service_data/state.dat`.
   - If the file exists and its contents start with the exact string `READY`, print exactly `HEALTHY` to standard output and exit with code 0.
   - If the file does not exist, cannot be read, or contains anything else, print exactly `CORRUPT` to standard output and exit with code 1.

3. **Backup Script**:
   Write a bash script at `/home/user/backup.sh` that creates a compressed tar archive of the `/home/user/service_data` directory. The archive must be saved to `/home/user/backup.tar.gz`. Ensure the script is executable.

4. **Automated Interactive Restore**:
   The system provides an interactive restore utility at `/home/user/restore_tool`. When run, it prompts:
   `Are you sure you want to restore? [y/N]: `
   If you answer `y`, it prompts:
   `Enter path to backup archive: `
   Write an Expect script at `/home/user/restore.exp` that launches `/home/user/restore_tool`, automatically answers `y` to the first prompt, and provides `/home/user/backup.tar.gz` to the second prompt. The Expect script should wait for the process to finish (expect EOF). Make the script executable.

Ensure all scripts and compiled binaries are placed at the exact paths specified.
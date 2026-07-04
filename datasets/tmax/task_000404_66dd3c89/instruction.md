You are a cloud architect migrating a legacy data processing service to a restricted user-space container environment. You do not have root access, but you need to recreate a robust environment simulating mount points, and you need a custom process supervisor written in C to ensure service availability. 

Complete the following three phases to migrate the service.

**Phase 1: Idempotent User-Space Mount Script**
Because you lack root privileges, you will simulate `fstab` mounts using directories and symlinks.
1. Create a configuration file at `/home/user/fstab.conf` with the following exact contents:
`/home/user/data_source /home/user/data_dest`
`/home/user/log_source /home/user/log_dest`
2. Write a bash script at `/home/user/setup_mounts.sh`. This script must read `/home/user/fstab.conf` line by line. For each line containing `<source_dir> <dest_dir>`, it must:
   - Ensure both directories exist (create them if they don't).
   - Create a symlink at `<dest_dir>/mnt` that points to `<source_dir>`.
   - The script must be completely idempotent (running it multiple times should not result in errors or nested symlinks).

**Phase 2: Custom C Process Supervisor**
Write a C program at `/home/user/supervisor.c` that acts as a process supervisor.
1. The program must accept arguments in the format: `./supervisor <max_retries> <command> [args...]`
2. It should use `fork()` and `execvp()` to run the specified command.
3. It must wait for the child process to finish.
4. If the child exits with status code 0, the supervisor should also exit with status code 0 immediately.
5. If the child exits with a non-zero status code, the supervisor must print exactly `[Supervisor] Restarting...\n` to `stdout`, and then restart the child process.
6. It should restart the child process up to `<max_retries>` times. If the child fails `<max_retries>` times (which means it executes a total of `<max_retries> + 1` times), the supervisor must exit with status code 1.
7. Compile the program to `/home/user/supervisor`.

**Phase 3: Deployment & Testing**
1. Create a mock failing service script at `/home/user/failing_service.sh` with the following contents:
```bash
#!/bin/bash
echo "Running service..."
exit 2
```
2. Make both scripts executable.
3. Run `/home/user/setup_mounts.sh`.
4. Execute the supervisor to run the failing service with 3 max retries, and redirect both `stdout` and `stderr` to `/home/user/migration_result.log` like this:
`./supervisor 3 /home/user/failing_service.sh > /home/user/migration_result.log 2>&1`
You are managing a user account authentication service that is currently failing. A local user-manager daemon is expected to create a Unix socket, but downstream services are failing to connect because the socket path is dynamically configured and currently unknown to the scheduling system.

Your task is to fix this by writing a Rust utility that determines the correct socket path from our configuration, configuring the environment, and setting up a scheduled job to continually report this path for downstream services.

Here are the requirements:

1. We have a pseudo-fstab file located at `/home/user/conf/fstab`. It contains various mount configurations. The authentication service creates its socket inside the mount point assigned to the device named `user_data`.
2. Write a Rust program at `/home/user/scripts/get_socket_path.rs`. This program must:
   - Read the environment variable `USERS_FSTAB` to get the path to the fstab file.
   - Parse the file and locate the line where the first column (device name) is exactly `user_data`.
   - Extract the second column (the mount point).
   - Print the exact string: `<mount_point>/auth.sock` (replacing `<mount_point>` with the extracted path) to standard output.
   - Do not print anything else.
3. Compile this Rust program to a binary named `/home/user/scripts/get_socket_path`.
4. Update the user's shell profile at `/home/user/.profile` to export the environment variable `USERS_FSTAB` with the value `/home/user/conf/fstab`.
5. Create a user cronjob (using `crontab`) that runs the compiled binary exactly every minute. The cronjob must redirect the standard output of the binary to `/home/user/socket_path.log`.

Ensure all directories exist (create `/home/user/scripts` and `/home/user/conf` if necessary). Write the pseudo-fstab file manually to test your code. Do not rely on root privileges.
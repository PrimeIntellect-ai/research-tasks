You are a Linux systems engineer tasked with hardening and fixing a local storage monitoring daemon. A recent deployment broke the service, causing the frontend (which relies on a specific Unix domain socket path) to fail to connect to the backend daemon, similar to an nginx 502 bad gateway error but via local sockets.

The application environment is located at `/home/user/app_env`.

Your objectives are:

1. **Backup Strategy:**
   Before making any changes, create a backup of the current configuration. 
   Create a gzip-compressed tarball of the `/home/user/app_env/config` directory and save it as `/home/user/app_env/backups/config_backup.tar.gz`.

2. **Link and Directory Structure Management:**
   The frontend expects to communicate with the backend via the socket file `/home/user/app_env/sockets/upstream.sock`. Currently, this is a broken symlink pointing to `/tmp/wrong_path.sock`.
   Update the symlink `/home/user/app_env/sockets/upstream.sock` so that it correctly points to the actual backend socket at `/home/user/app_env/run/backend.sock`.

3. **Storage Monitoring (C++ Programming):**
   The backend source code is located at `/home/user/app_env/src/backend.cpp`. The socket boilerplate is already written, but the storage monitoring logic is missing.
   Edit `/home/user/app_env/src/backend.cpp`. Look for the `// TODO: Implement storage check` comment. Use the standard C++ `<filesystem>` library to query the available space (in bytes) on the `/home/user` directory. 
   When the daemon receives the string `"STATUS\n"`, it must respond with the exact format: `OK: <bytes_available>\n` (where `<bytes_available>` is the available capacity integer).

4. **Build, Run, and Verify:**
   - Compile the backend code using `g++` (ensure you use `-std=c++17`). Save the executable to `/home/user/app_env/bin/backend`.
   - Run the compiled `backend` daemon in the background. (It will automatically bind to `/home/user/app_env/run/backend.sock`).
   - Query the daemon to ensure it works. Send the string `"STATUS\n"` to the frontend socket (`/home/user/app_env/sockets/upstream.sock`) using `nc -U` (or `socat`).
   - Save the exact output of this query to `/home/user/app_env/verify.log`.

Do not hardcode the available bytes in your C++ program; it must be calculated dynamically.
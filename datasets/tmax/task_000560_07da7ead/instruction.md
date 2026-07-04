You are tasked with debugging and fixing a configuration backup pipeline that is malfunctioning due to a directory traversal bug and broken service integrations. 

The system consists of three components located in `/app/`:
1. **Nginx** (running on port 8080): Serves as the configuration upload endpoint. It is supposed to log uploads to `/app/logs/update.log` in a specific multi-line format, but its configuration `/app/nginx/nginx.conf` is currently broken and failing to route requests to the correct log.
2. **Redis** (running on port 6379): Used as the state store for the backup agent.
3. **Backup Agent** (`/app/backup_agent/agent.c`): A C daemon that parses the multi-line log records from `/app/logs/update.log`, extracts the target directories, reads the configuration files, strips a 16-byte binary header from each file, and creates a zlib-compressed stream of the bodies. It saves the final compressed archive to `/home/user/backup.gz`.

**The Problem:**
1. Nginx is not logging the expected multi-line format correctly. You need to fix `/app/nginx/nginx.conf` so that HTTP POSTs to `/upload` log the required multi-line format (you can find the expected format parsing logic in `agent.c`).
2. There is a symlink loop in the configuration directories (`/app/configs/legacy -> /app/configs`). The `agent.c` uses `stat()` instead of `lstat()` and blindly follows symlinks, causing an infinite loop. As a result, the compressed stream processes gigabytes of duplicate data until it crashes or fills the disk.

**Your Objectives:**
1. Fix `agent.c` to properly use `lstat()`, detect symlinks (`S_ISLNK`), and skip them to prevent the infinite loop.
2. Recompile the C program using `gcc -o agent agent.c -lz`.
3. Fix the Nginx configuration to ensure the `update.log` is generated correctly when requests are made.
4. Restart the Nginx service and the Redis service (they have standard init scripts in `/app/scripts/`).
5. Run the backup agent against the provided test log.

The automated verification will check the size of the generated `/home/user/backup.gz` file. A successful fix will result in a small, correctly compressed archive containing only the unique regular files, whereas a failure will result in an oversized file or a timeout.
You are an infrastructure engineer automating the provisioning of a local user-space environment. You need to write two Python scripts to handle load balancer configuration, storage monitoring, and backups without using root privileges.

**Phase 1: Idempotent Reverse Proxy Configuration**
Write a Python script at `/home/user/setup_proxy.py`. This script must idempotently generate an Nginx configuration file at `/home/user/nginx.conf`. 
The Nginx configuration must meet these exact requirements:
- Run entirely in user-space (no root required).
- Set the PID file to `/home/user/nginx.pid`.
- Set the error log to `/home/user/error.log` and access log to `/home/user/access.log`.
- Configure an `events` block (default settings are fine).
- Configure an `http` block with a server listening on port `8080`.
- The server on port `8080` must proxy all requests (`location /`) to an upstream group named `backend`.
- The `backend` upstream group must load balance between `127.0.0.1:8081` and `127.0.0.1:8082`.

Your `setup_proxy.py` script must be idempotent: it should only write or overwrite `/home/user/nginx.conf` if the file does not exist or its current contents differ from the desired configuration. After generating the file, the script should print "CONFIG_UPDATED" if it made changes, or "CONFIG_UNCHANGED" if the file was already correct.
Run your script so that `/home/user/nginx.conf` is generated.

**Phase 2: Storage Monitoring and Backup Strategy**
Write a second Python script at `/home/user/backup.py`. This script will monitor a storage directory and perform backups conditionally based on a simulated disk quota.
1. The script must target the directory `/home/user/storage/` (you should create this directory).
2. It must calculate the total size of all files inside `/home/user/storage/` in bytes.
3. **Quota Check:** If the total size exceeds 50 Megabytes (50 * 1024 * 1024 bytes), the script must NOT perform a backup. Instead, it must write the exact string `QUOTA_EXCEEDED` to a log file at `/home/user/backup.log`.
4. **Backup Execution:** If the total size is 50 Megabytes or less, the script must create a gzipped tarball of the `/home/user/storage/` directory at `/home/user/backups/storage_backup.tar.gz` (you should create the `/home/user/backups/` directory). After creating the archive, it must write the exact string `BACKUP_SUCCESS` to `/home/user/backup.log`.

To complete the task:
- Create the necessary directories: `/home/user/storage/` and `/home/user/backups/`.
- Create a dummy file of 10MB inside `/home/user/storage/` named `dummy.txt` (e.g., using `dd`).
- Run `/home/user/setup_proxy.py` to generate the Nginx config.
- Run `/home/user/backup.py` to trigger a successful backup and generate the log.

Leave everything in this final state for verification.
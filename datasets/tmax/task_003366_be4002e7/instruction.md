You are an automated backup operator. Your goal is to build a robust, automated pipeline that tests restored backups by exposing them via a local reverse proxy. You must write a Python script to handle the logic, configure a user-space Nginx reverse proxy, and schedule the script to run automatically.

Since you do not have root access, everything must run in user space under the user `user` (home directory: `/home/user`).

Here are the requirements:

1. **Directory Structure**: 
   Ensure the following directories exist in `/home/user/`:
   - `restore_inbox/` (where new backups arrive)
   - `restore_active/` (where backups are extracted)
   - `restore_processed/` (where tarballs are moved after processing)
   - `proxy_conf/` (Nginx location snippet configurations)
   - `nginx_logs/` (for Nginx error and access logs)

2. **Nginx Reverse Proxy**:
   Create a main Nginx configuration file at `/home/user/nginx.conf` that:
   - Runs as the current user (do not use the `user` directive).
   - Stores its PID file at `/home/user/nginx.pid`.
   - Stores access and error logs in `/home/user/nginx_logs/`.
   - Listens on `127.0.0.1:8080`.
   - Includes all `.conf` files from `/home/user/proxy_conf/` inside its `server` block.
   - Start this Nginx instance in the background.

3. **Python Restore Tester (`/home/user/restore_tester.py`)**:
   Write a Python script that performs the following steps when executed:
   - Scans `/home/user/restore_inbox/` for files ending in `.tar.gz`.
   - For each archive (e.g., `backup_2023.tar.gz`):
     - Extracts the contents into a new directory: `/home/user/restore_active/backup_2023/`.
     - Recursively sets strict permissions on the extracted directory: directories must be `750` and files must be `640`.
     - Assigns an Access Control List (ACL) to the extracted directory and all its contents granting the user `nobody` read access (`r-x` for dirs, `r--` for files). Ignore errors if the filesystem does not support ACLs, but the `setfacl` command/logic must be present.
     - Dynamically finds an available high port starting from `9000`.
     - Launches a background web server for that specific directory (`python3 -m http.server <PORT> --directory /home/user/restore_active/backup_2023/`).
     - Generates an Nginx configuration snippet at `/home/user/proxy_conf/backup_2023.conf` with the following format:
       ```
       location /backup_2023/ {
           proxy_pass http://127.0.0.1:<PORT>/;
       }
       ```
     - Moves the original `.tar.gz` file to `/home/user/restore_processed/`.
   - After processing any new archives, if changes were made, it must reload the Nginx configuration using `nginx -c /home/user/nginx.conf -s reload`.

4. **Scheduling**:
   - Install a user-level crontab that executes `/home/user/restore_tester.py` every minute. 
   - Route both stdout and stderr of the cron job to `/home/user/cron_tester.log`.

5. **Finalization**:
   - When you have completed all configurations, written the script, started Nginx, and installed the crontab, write the word `READY` to `/home/user/setup_done.txt`.
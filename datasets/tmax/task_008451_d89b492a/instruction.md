You are a Cloud Architect migrating legacy applications to a new infrastructure. As part of the migration strategy, you need to set up a local staging environment that combines a reverse proxy, strict directory structures, process monitoring, and automated backups, all running in user-space (without root privileges).

Your task is to implement this staging environment in `/home/user/migration`. 

Please perform the following steps:

1. **Directory Structure and Links**:
   - Create a base directory `/home/user/migration/app_data/`. Inside it, create three directories: `server1`, `server2`, `server3`.
   - Create a directory `/home/user/migration/active_apps/`.
   - Create symlinks inside `/home/user/migration/active_apps/` named `app1`, `app2`, and `app3` pointing to their respective `server1`, `server2`, and `server3` directories in `app_data`.

2. **Load Balancer Configuration (Nginx)**:
   - Create an Nginx configuration file at `/home/user/migration/nginx.conf`.
   - This configuration must run entirely in user space. Set the `pid`, `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, `scgi_temp_path`, `access_log`, and `error_log` directives to paths inside a new directory `/home/user/migration/nginx_run/` (which you should create).
   - Configure Nginx to listen on `127.0.0.1:8080`.
   - Set up an `upstream` block named `backend_cluster` that load balances requests round-robin across `127.0.0.1:8081`, `127.0.0.1:8082`, and `127.0.0.1:8083`.
   - Route all traffic (`/`) to this `backend_cluster`.

3. **Process Monitor and Backup Script (Python)**:
   - Write a Python script at `/home/user/migration/monitor.py`.
   - When executed with a command-line argument `--check`, the script should test if ports `8081`, `8082`, and `8083` on `127.0.0.1` are actively listening.
   - **Log Configuration**: Use Python's `logging` module with a `RotatingFileHandler`. Log to `/home/user/migration/logs/monitor.log`. Configure it to rotate at 1024 bytes (1 KB) and keep up to 3 backup files. Format: `[YYYY-MM-DD HH:MM:SS] - LEVEL - MESSAGE`.
   - **Logic**: 
     - If all three ports are listening, log: `INFO - All backend servers are healthy.`
     - If any port is NOT listening, log: `ERROR - Backend port <PORT> is down. Initiating backup.`
     - **Backup Strategy**: Immediately after logging a down port, the script must create a compressed tarball (`.tar.gz`) of the `/home/user/migration/active_apps/` directory and save it as `/home/user/migration/backups/apps_backup_<timestamp>.tar.gz` (timestamp format: `YYYYMMDD_HHMMSS`). Create the `backups` and `logs` directories if they don't exist.

Ensure your code handles imports and exceptions gracefully. You do not need to actually start Nginx or the backend applications—we will test your `monitor.py` and configuration programmatically.
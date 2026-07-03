You are acting as a container specialist managing a mock microservice deployment. The configuration files for our services have been mixed up, causing network routing failures. You need to back up the existing state, write an idempotent Bash script to fix the configurations, and generate a report.

The services are located in `/home/user/services/` with the following subdirectories: `db`, `auth`, `api`, and `web`.
Inside each directory, there is a configuration file named `service.conf`.

Currently, the `service.conf` files contain incorrect `LISTEN_PORT` and `UPSTREAM_URL` values.

Perform the following tasks using only Bash built-ins and standard Linux utilities:

1. **Backup**: Create a compressed tarball backup of the `/home/user/services/` directory at `/home/user/services_backup.tar.gz` before making any changes.

2. **Idempotent Configuration**: Write and execute a Bash script at `/home/user/fix_network.sh` that updates the `service.conf` files to exactly match the following topology:
   - **db**: `LISTEN_PORT=9001` (No upstream)
   - **auth**: `LISTEN_PORT=9002`, `UPSTREAM_URL=http://localhost:9001`
   - **api**: `LISTEN_PORT=9003`, `UPSTREAM_URL=http://localhost:9002`
   - **web**: `LISTEN_PORT=9004`, `UPSTREAM_URL=http://localhost:9003`
   
   Your script must be idempotent (running it multiple times should result in the exact same file state) and should modify the values in-place without removing other unrelated configuration lines that might exist in those files.

3. **Report Generation**: Write a bash script `/home/user/generate_report.sh` that reads the updated `service.conf` files and creates a log file at `/home/user/network_report.log`.
   The log file must contain exactly these lines in this order:
   ```
   db:9001:none
   auth:9002:http://localhost:9001
   api:9003:http://localhost:9002
   web:9004:http://localhost:9003
   ```
   (If a service has no upstream, output `none`).

Execute both scripts so that `/home/user/services_backup.tar.gz`, the corrected `service.conf` files, and `/home/user/network_report.log` are all present.
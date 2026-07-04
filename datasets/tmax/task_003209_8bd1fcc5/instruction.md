You are acting as a capacity planner who needs to analyze the resource usage of a virtualized application stack, expose the metrics securely, and ensure they are backed up. 

Your environment is a standard Linux system. You must complete the following deployment and configuration steps. Do not use `sudo` or require root privileges; all configurations must run in user space.

1. **Virtualization Management:**
   Start a background QEMU process to simulate a workload. Use the following exact parameters:
   - Architecture: `qemu-system-x86_64`
   - Memory: 128 MB
   - VNC: Listen on `127.0.0.1` display `5` (port 5905)
   - Daemonize the process.
   - Write the PID to `/home/user/qemu.pid`.

2. **C++ Resource Analyzer:**
   Create a C++ program at `/home/user/capacity_planner/analyzer.cpp` that acts as your metric collector.
   - The program must read the PID from `/home/user/qemu.pid`.
   - It must then read the virtual memory size (the first value) from `/proc/<pid>/statm` for that QEMU process.
   - It must output this metric as a JSON string: `{"vmem_pages": <value>}`.
   - The JSON string must be written to a file path specified by the environment variable `METRICS_FILE`.
   - Compile this program to `/home/user/capacity_planner/analyzer`.
   - Append a line to `/home/user/.bash_profile` to export `METRICS_FILE=/home/user/metrics/current.json`.
   - Execute the compiled analyzer (ensuring the environment variable is passed) so that the output file `/home/user/metrics/current.json` is generated.

3. **Secure Web Server Setup:**
   Expose the `/home/user/metrics/` directory securely.
   - Generate a self-signed RSA certificate (2048-bit) valid for 365 days. Place the certificate at `/home/user/tls/cert.pem` and the private key at `/home/user/tls/key.pem`.
   - Create a local, unprivileged Nginx configuration file at `/home/user/nginx.conf`.
   - The Nginx server must listen on port `8443` using SSL/TLS with the generated certificates.
   - It must serve files directly from the `/home/user/metrics/` directory.
   - Ensure the Nginx config stores its `pid`, `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path` in `/home/user/nginx_temp/` to avoid permission errors. It should also log to `/home/user/nginx_temp/access.log` and `error.log`.
   - Start Nginx using this configuration file.

4. **Backup Strategy:**
   Create a shell script at `/home/user/backup.sh` that, when run, creates a tarball of the current metrics.
   - It must compress `/home/user/metrics/current.json` into `/home/user/backups/metrics_backup.tar.gz`.
   - Run the script once so the backup file is created.

Ensure all directories (`/home/user/capacity_planner`, `/home/user/metrics`, `/home/user/tls`, `/home/user/nginx_temp`, `/home/user/backups`) are created before generating files inside them. Keep the QEMU and Nginx processes running in the background.
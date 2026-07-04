As a capacity planner, I need to baseline the storage footprint of a new secure web service deployment structure before we scale it to our production servers. 

Write a bash script at `/home/user/setup_baseline.sh` that automates this baseline setup and measurement. When executed, your script must perform the following actions exactly:

1. Create the following directory structure: 
   - `/home/user/service/www`
   - `/home/user/service/logs`
   - `/home/user/service/certs`

2. Create a symbolic link at `/home/user/service/current_logs` that points to the `/home/user/service/logs` directory.

3. Generate a 2048-bit RSA self-signed TLS certificate (`cert.pem`) and an unencrypted private key (`key.pem`) in the `/home/user/service/certs` directory. It should be valid for 30 days and have the subject `/CN=capacity.local`.

4. Create a logrotate configuration file at `/home/user/service/logrotate.conf`. This configuration should apply to `/home/user/service/logs/*.log` and specify that logs should be rotated `daily`, keep `7` backups, and use `compress`.

5. Generate a dummy log file at `/home/user/service/logs/access.log` containing exactly 1000 lines of the text: `dummy log entry`

6. Finally, the script must compute the total apparent size in bytes of the `/home/user/service` directory (using `du -sb /home/user/service`) and save *only* that numeric byte value to `/home/user/baseline_size.txt`.

Ensure your script is executable (`chmod +x`). You do not need root privileges for this task. Use standard Linux utilities (`mkdir`, `ln`, `openssl`, `echo`, `du`, etc.).
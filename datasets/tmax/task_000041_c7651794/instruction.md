You are a system administrator diagnosing a failing user-level systemd service on a Linux server. 

The service, `micro-proxy.service`, is supposed to start a lightweight Python reverse proxy and load balancer. However, it currently fails to start. 

Your tasks are:
1. Diagnose why `systemctl --user start micro-proxy.service` fails.
2. Identify and resolve the issues preventing the service from starting. The issues involve:
   - A storage monitoring script enforcing a disk quota check on the proxy logs.
   - A directory structure and symlink configuration issue preventing the proxy from finding its configuration file.
3. Write an idempotent shell script at `/home/user/repair.sh` that automatically applies these fixes (clearing/managing the offending storage space, and fixing the configuration symlinks so they point to the correct active configuration). The script must be safe to run multiple times.
4. Start the service successfully.
5. Save the output of the command `systemctl --user is-active micro-proxy.service` into `/home/user/service_status.txt`.

Ensure your `repair.sh` script is executable. You have access to the terminal to explore the system logs and structure to uncover the exact paths and limits involved.
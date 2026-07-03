You are a system administrator maintaining a custom server environment. A daemon is currently failing because its generated configuration points to the wrong Unix socket path.

You need to fix the configuration generator, apply the fix, and create a simple log rotation script for the daemon's logs.

Here are the details:
1. There is a discovery log located at `/home/user/app/discovery.log`. Inside this file, there is a single line containing `BIND_ADDR=` followed by the actual socket path the daemon is using (e.g., `BIND_ADDR=/tmp/run/...`).
2. There is a configuration generator script at `/home/user/app/generate_config.sh`. It currently hardcodes `SOCKET_PATH="/tmp/app.sock"`. 
3. You must modify `/home/user/app/generate_config.sh` so that `SOCKET_PATH` is set to the correct socket path found in the discovery log.
4. Execute `/home/user/app/generate_config.sh`. This will generate the file `/home/user/app/nginx-upstream.conf`.
5. The daemon writes logs to `/home/user/app/daemon.log`. Write a bash script at `/home/user/app/rotate.sh` that performs a manual log rotation:
   - It must rename the existing `/home/user/app/daemon.log` to `/home/user/app/daemon.log.1`
   - It must create a new, empty `/home/user/app/daemon.log`
   - It must append exactly the text `--- LOG ROTATED ---` (followed by a newline) to the newly created `/home/user/app/daemon.log`
6. Make your `/home/user/app/rotate.sh` script executable and run it once.

Ensure all paths used in your commands and scripts are absolute.
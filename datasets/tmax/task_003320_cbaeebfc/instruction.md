You are acting as a network engineer troubleshooting a flaky connection issue on our QEMU/VNC virtualized routers. We have captured a diagnostic video of the VNC session during a network test, and we need to automate the extraction of failure events and set up a temporary user-space reverse proxy to route around the failures.

You must perform the following tasks entirely in user-space without `sudo`:

1. **Virtualization/Filesystem extraction:**
   We have a raw ext4 filesystem image at `/app/router_fs.ext4`. It contains a file at `/etc/backend_ips.conf` which lists the IP addresses and ports of our backup upstream servers. Since you don't have root access to `mount` it, use user-space tools (like `debugfs` or `guestfish`) to extract the contents of `/etc/backend_ips.conf`.
   Additionally, write exactly one valid `fstab` entry to `/home/user/router_fstab` that an admin could use later to mount this image at `/mnt/router` using a loopback device, read-only, allowing users to mount it.

2. **Video Analysis (Network Drops):**
   The diagnostic video is located at `/app/vnc_capture.mp4`. It is a 30fps screen recording. During network outages, the diagnostic tool flashes a solid Red square (RGB: `255, 0, 0`) in the top-left corner (from pixel 0,0 to 50,50). When the network is stable, this square is Green (RGB: `0, 255, 0`).
   Write a Bash script, or a script executed via Bash (using ffmpeg, Python, etc.), that processes this video and outputs the frame indices (0-indexed) where the network is DOWN (i.e., the square is predominantly red). 
   Write these frame numbers, one per line, to `/home/user/down_frames.txt`.

3. **Reverse Proxy Configuration:**
   Using the backend servers extracted from the filesystem image in step 1, generate an Nginx configuration file at `/home/user/lb.conf`. 
   The configuration must:
   - Run in the foreground (`daemon off;`)
   - Store its pid file at `/home/user/nginx.pid`
   - Log errors to `/home/user/error.log`
   - Listen on `127.0.0.1:8080`
   - Load balance incoming HTTP requests across all the backend servers listed in the extracted `/etc/backend_ips.conf` file using a simple round-robin approach.

Your final evaluation will heavily depend on the accuracy of the extracted frame indices in `/home/user/down_frames.txt`. Ensure your detection is precise.
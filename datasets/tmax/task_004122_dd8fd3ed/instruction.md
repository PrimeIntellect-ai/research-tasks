You are acting as an infrastructure engineer automating the provisioning of a lightweight, user-space deployment. Since we do not have root access on this environment, we are simulating a deployment stack using user-space tools, mock configuration files, and a custom-built TCP proxy in C.

Your task consists of several deployment phases:

**Phase 1: Configuration Management & Fstab Mock**
1. Create a directory `/home/user/app_deployment/config`.
2. Inside it, create a file named `fstab.mock` that acts as our simulated filesystem table. Add exactly one line to this file to simulate bind-mounting `/home/user/app_deployment/storage` to `/home/user/app_deployment/container_data` with default options. The format must exactly match standard `/etc/fstab` format (5 fields separated by spaces/tabs: `<file system> <dir> <type> <options> <dump> <pass>`). Use `none` for the type, `bind` for options, and `0 0` for dump and pass.
3. Create both directories referenced in the fstab line (`storage` and `container_data`). Inside `storage`, create a file `index.html` with the exact text: `DEPLOYMENT_SUCCESS`.

**Phase 2: Custom C Port Forwarder (Firewall/Routing alternative)**
Instead of using iptables (which requires root), you must write a simple TCP proxy in C.
1. Write a C program at `/home/user/app_deployment/src/proxy.c`.
2. The program must:
   - Listen for incoming TCP connections on `127.0.0.1` port `8080`.
   - Accept a single connection at a time.
   - When a client connects, immediately connect to `127.0.0.1` port `9090`.
   - Read up to 1024 bytes from the client and forward it to port 9090.
   - Read up to 1024 bytes from port 9090 and forward it back to the client.
   - Close both sockets and exit cleanly after handling one request (for testing purposes, it only needs to handle one request and then terminate).
3. Compile it to `/home/user/app_deployment/bin/proxy_server` using `gcc`.

**Phase 3: Container Lifecycle Mock**
We will simulate a containerized application using a Python web server.
1. Write a bash script `/home/user/app_deployment/scripts/start_stack.sh`.
2. The script must:
   - Copy the contents of `/home/user/app_deployment/storage/` to `/home/user/app_deployment/container_data/` (simulating the mount step).
   - Start a Python HTTP server on port `9090` serving the directory `/home/user/app_deployment/container_data` in the background.
   - Start your compiled `proxy_server` in the background.
   - Wait 2 seconds to ensure services are up.
   - Use `curl` to fetch `http://127.0.0.1:8080/index.html` and save the output to `/home/user/app_deployment/logs/test_request.log`.

**Phase 4: Email Server Configuration Notification**
1. Once the stack is simulated, create a deployment notification email mimicking an SMTP payload.
2. Create a file `/home/user/app_deployment/mail/deployment_alert.eml` with the following exact format:
```
From: deploybot@localhost
To: sysadmin@localhost
Subject: Deployment Status

Proxy server is running on port 8080.
Backend container is on port 9090.
Log output captured.
```

Ensure all directories (`config`, `src`, `bin`, `scripts`, `logs`, `mail`) are created under `/home/user/app_deployment/`. Ensure the bash script has executable permissions. You may run the bash script to verify it works and generates the required log file.
You are an infrastructure engineer automating the provisioning and monitoring of a lightweight virtual machine. Your task is to start a QEMU instance, write a custom C program to monitor its process status, and expose this status securely via an HTTPS web server. 

Perform the following steps exactly as specified. You do not have root access. Work entirely within `/home/user`.

1. **Virtual Machine Setup**:
   Create a directory `/home/user/web/`.
   Start a headless QEMU instance using `qemu-system-x86_64`. It should be an empty PC machine, suspended at startup (`-S`), daemonized (`-daemonize`), with no graphics console (`-nographic`), but with a VNC server listening on display `5` (which corresponds to port 5905). Have QEMU write its PID to `/home/user/vm.pid`.

2. **C Process Monitor**:
   Write a C program at `/home/user/monitor.c`.
   This program must:
   - Read the integer PID from `/home/user/vm.pid`.
   - Check if the process with that PID is currently running (e.g., using `kill(pid, 0)`).
   - If the process is running, write the exact string `VNC_PORT=5905\nSTATUS=RUNNING\n` to `/home/user/web/status.txt`.
   - If the process is NOT running, write the exact string `STATUS=STOPPED\n` to `/home/user/web/status.txt`.
   
   Compile this program to `/home/user/monitor` using `gcc`. Run the executable once so that `/home/user/web/status.txt` is populated.

3. **TLS Web Server**:
   Generate a self-signed RSA 2048-bit certificate and unencrypted private key. Save them as `/home/user/web/cert.pem` and `/home/user/web/key.pem` respectively.
   Write a Python 3 script at `/home/user/web/server.py` that acts as a simple HTTPS server. It should:
   - Serve the contents of the `/home/user/web/` directory.
   - Bind to `0.0.0.0` on port `8443`.
   - Use the generated `cert.pem` and `key.pem` to wrap the socket in TLS.
   
   Execute this Python script in the background so it remains running.

Ensure the QEMU instance and the Python web server are both running in the background when you complete your task.
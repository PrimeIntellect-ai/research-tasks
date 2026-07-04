You are an SRE investigating an outage. Our newly deployed multi-service architecture in `/home/user/app/` is failing. 

The architecture consists of:
1. An Nginx reverse proxy configured via `/home/user/app/nginx.conf` (listening on 127.0.0.1:8080).
2. A custom backend written in C (`/home/user/app/backend.c`). For legacy compatibility reasons, this backend must be compiled for ARM64 and executed via user-mode QEMU (`qemu-aarch64-static`).

Currently, making a request to Nginx (`curl http://127.0.0.1:8080/`) returns a 502 Bad Gateway error. Additionally, under moderate load, the backend completely hangs.

Your objectives:
1. **Fix the configuration and code**: 
   - Inspect `/home/user/app/nginx.conf` and `/home/user/app/backend.c`. There is a mismatch in the upstream configuration and a severe performance bug (an artificial delay) in the C code.
   - Fix the port mismatch so Nginx can communicate with the backend.
   - Remove the performance bottleneck in `backend.c`.
2. **Re-deploy the backend**:
   - Compile the C backend using `aarch64-linux-gnu-gcc -static -o /home/user/app/backend_arm /home/user/app/backend.c`.
   - Start the backend in the background using `qemu-aarch64-static /home/user/app/backend_arm`.
   - Start Nginx using `nginx -c /home/user/app/nginx.conf -p /home/user/app/`.
3. **Write a Monitoring Script**:
   - Create a script at `/home/user/app/monitor.sh` that acts like a custom process monitor. It should check `http://127.0.0.1:8080/` using `curl`. If it receives a 502 or connection refused, it should automatically kill any existing `backend_arm` processes and restart it using QEMU.

Ensure the final system is highly responsive. We will run an automated load test against `http://127.0.0.1:8080/` to verify it can handle concurrent requests without timing out.
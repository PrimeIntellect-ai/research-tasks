You are a network engineer troubleshooting a custom user-space network proxy and backend service setup. The backend service needs to be containerized, traffic needs to be forwarded to it, and a custom C-based healthcheck utility needs to be repaired to verify connectivity and access controls.

Your environment contains an Apptainer image at `/home/user/busybox.sif` and a broken healthcheck source file at `/home/user/healthcheck.c`.

Perform the following steps:

1. **Container Lifecycle Management**: Start an Apptainer instance named `backend_svc` using the `/home/user/busybox.sif` image. Inside this instance, run a background process that listens on TCP port `9090` and continuously serves the text `HELLO_FROM_BACKEND` to any connected client. (Hint: you can use `nc -l -p 9090` in a loop).

2. **Port Forwarding**: On the host system, set up a user-space port forward using `socat`. Listen on TCP port `8080` (bind to `127.0.0.1`) and forward all incoming connections to the containerized service on `127.0.0.1:9090`. Ensure it can handle multiple connections (forking).

3. **User Administration Simulation**: The healthcheck utility requires an access control file. Create a file at `/home/user/app_users.txt` containing exactly one line:
   `admin:network_engineers`

4. **C Code Debugging**: The file `/home/user/healthcheck.c` is supposed to read `/home/user/app_users.txt`, verify that the user `admin` belongs to the `network_engineers` group, and then connect to the proxy on port `8080` to read the backend banner. However, the code has a few bugs: it tries to connect to the wrong port (8081) and has a string matching error when parsing the user file.
   - Fix the bugs in `/home/user/healthcheck.c`.
   - Compile it to an executable named `/home/user/healthcheck`.
   - Execute the compiled program. It should output the banner received from the proxy.
   
5. **Final Output**: Redirect the standard output of the successful `/home/user/healthcheck` run into `/home/user/result.log`.

Do not use `sudo` or root privileges for any of these tasks. Ensure your background processes (`socat` and the containerized `nc`) remain running when you complete the task.
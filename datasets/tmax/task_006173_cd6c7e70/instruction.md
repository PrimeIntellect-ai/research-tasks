You are a cloud architect migrating a legacy payment application to a new environment. Since you do not have root access, you need to set up the services in your home directory.

You have been provided with the source code for the backend and a simple load balancer/reverse proxy, as well as a legacy configuration file.

Here is your task:

1. **Text Processing**: 
   Read `/home/user/migration/legacy_config.txt`. The file format is `service_name:port:environment:status`. 
   Use text processing tools to find the port number for the `payment` service that is in the `production` environment and has an `active` status.
   Save just this port number to `/home/user/deploy/backend_port.txt`.

2. **Compilation & Directory Structure**:
   Compile the C++ source files located in `/home/user/migration/src/`:
   - Compile `backend.cpp` to an executable named `backend_app`.
   - Compile `proxy.cpp` to an executable named `proxy_app`.
   
   Create the following directory structure:
   - `/home/user/deploy/bin/`
   - `/home/user/deploy/logs/`
   - `/home/user/deploy/run/`
   
   Do NOT move the compiled executables. Instead, create symbolic links to `backend_app` and `proxy_app` inside `/home/user/deploy/bin/`.

3. **Permission & ACL Management**:
   We need to ensure that log files can be audited. Use Access Control Lists (ACLs) to grant the `users` group read and execute permissions (`r-x`) to the `/home/user/deploy/logs/` directory. Also, set the default ACL for this directory so that any newly created files inside it inherit read permissions (`r--`) for the `users` group.

4. **Service Lifecycle & Proxy Setup**:
   Since systemd might not be fully functional for non-root users in this container, create a custom init-style bash script at `/home/user/deploy/manage.sh` with executable permissions.
   The script must accept exactly one argument: `start` or `stop`.
   
   When run with `start`:
   - It should launch `/home/user/deploy/bin/backend_app <PORT>` in the background, where `<PORT>` is the port you extracted in step 1.
   - It should redirect the backend's standard output and error to `/home/user/deploy/logs/backend.log`.
   - It should save the backend's PID to `/home/user/deploy/run/backend.pid`.
   - It should then launch `/home/user/deploy/bin/proxy_app 8080 <PORT>` in the background (which listens on 8080 and proxies to the backend port).
   - It should redirect the proxy's standard output and error to `/home/user/deploy/logs/proxy.log`.
   - It should save the proxy's PID to `/home/user/deploy/run/proxy.pid`.

   When run with `stop`:
   - It should read the PIDs from the respective files in `/home/user/deploy/run/` and terminate the processes.
   - It should delete the `.pid` files.

5. **Final Execution**:
   Run `/home/user/deploy/manage.sh start` to leave the services running.
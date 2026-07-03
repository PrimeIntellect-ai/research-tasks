You are an infrastructure engineer automating the provisioning of a custom C++ micro-fileserver. 

We have a vendored C++ file server located at `/app/vendored/microserver`. However, the build is currently broken due to a configuration error, and the deployment needs to be completely automated without requiring root privileges. 

Please perform the following tasks to get the system operational:

1. **Fix and Build the Server**: 
   The C++ project in `/app/vendored/microserver` contains a `Makefile` and `server.cpp`. It currently fails to compile. Identify the build configuration issue in the Makefile, fix it, and compile the application. The resulting binary must be placed at `/home/user/microserver_bin`.

2. **Filesystem Setup**:
   Create a directory `/home/user/public_html`. Inside this directory, create a file named `index.html` with the exact content: `DEPLOYMENT_SUCCESS`. Create another file named `data.txt` with the exact content: `SENSITIVE_DATA`.

3. **Timezone and Locale Configuration**:
   The server relies on specific environment variables to format its internal timestamps correctly. Create a robust Bash script at `/home/user/start_server.sh` that:
   - Sets the timezone variable `TZ` to `Pacific/Auckland`.
   - Sets the locale variable `LC_ALL` to `en_NZ.UTF-8`.
   - Starts the `/home/user/microserver_bin` in the background. The server binary takes two arguments: the port to listen on and the base directory to serve. Configure it to listen on `127.0.0.1:9090` and serve `/home/user/public_html`.
   - Ensure the script handles errors gracefully (e.g., fails if the binary doesn't exist).

4. **Port Forwarding**:
   The external load balancer expects the service to be available on port `8080`, but our server must run on `9090`. Since you do not have root access to configure `iptables`, run a background `socat` process that forwards TCP traffic from `127.0.0.1:8080` to `127.0.0.1:9090`.

5. **Health Monitoring Script**:
   Write a monitoring script at `/home/user/monitor.sh`. This script should:
   - Perform an HTTP GET request to `http://127.0.0.1:8080/health` (the server handles this route automatically).
   - If the curl request succeeds (returns an HTTP 200), overwrite the file `/home/user/status.log` with the exact text `UP`.
   - Run this script in the background so it continuously checks the endpoint once every 2 seconds.

Ensure all services (the C++ server, the socat forwarder, and the monitor script) are running in the background when you finish your interaction.
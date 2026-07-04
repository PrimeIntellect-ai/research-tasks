You are a container specialist managing microservices. We have a legacy C++ microservice vendored at `/app/legacy-svc` that needs to be configured, compiled, and exposed. Complete the following deployment steps:

1. **Text Processing for Configuration**:
   The service requires a header file defining its endpoint route. Read the file `/app/routes.txt`. Find the line that begins with `ACTIVE: ` and extract the route path that follows it. Use text processing pipelines (like `awk` or `sed`) to generate a C++ header file at `/app/legacy-svc/route.h` containing exactly:
   `#define ROUTE_PATH "<extracted_route>"`

2. **Fix and Compile**:
   The service uses a Makefile for compilation. However, the `Makefile` is currently broken—it is missing a standard GCC threading flag required by the underlying HTTP library, causing compilation to fail. Identify the missing compiler flag, fix the `/app/legacy-svc/Makefile`, and run `make` to compile the `server` binary. 

3. **Service Execution & Logging**:
   Run the compiled binary (`/app/legacy-svc/server`) in the background. It will automatically bind to `127.0.0.1:8080` and append its logs to `/home/user/app.log`. 

4. **Port Forwarding**:
   Because the container environment restricts direct access to `127.0.0.1:8080`, use `socat` to create a user-space port forward. Forward incoming TCP traffic from `0.0.0.0:9090` to the service running at `127.0.0.1:8080`. Run this `socat` process in the background.

5. **Log Rotation**:
   To prevent disk quota issues from unbounded logs, create a user-space logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/app.log`. Configure it with the following rules: 
   - rotate daily
   - keep exactly 3 backups (`rotate 3`)
   - compress old logs
   - ignore missing log files (`missingok`)
   - size threshold of 10M

Ensure both the `server` and `socat` processes are running when you finish.
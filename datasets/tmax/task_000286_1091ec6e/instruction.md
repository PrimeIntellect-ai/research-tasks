You are managing a microservices deployment as a container specialist. We have a custom C++ time-reporting microservice that we are deploying locally. However, the vendored source code has a few configuration issues, the monitoring script writes to the wrong location, and the load balancer needs to be configured from scratch. 

Your objectives are to fix the C++ microservice, set up a pseudo-cron health monitor, and configure an Nginx reverse proxy.

**Step 1: Fix and Compile the Vendored Package**
We have vendored the source code for our microservice at `/app/tz-server-1.0`. 
1. The service fails to compile due to a deliberate configuration issue in the `Makefile`. Identify and fix the perturbation (hint: it requires a specific C++ standard to compile).
2. Compile the service. The resulting binary should be named `tz-server`.

**Step 2: Microservice Deployment & Timezone Configuration**
1. Start two instances of the `tz-server` binary in the background. 
2. They must listen on `127.0.0.1:8081` and `127.0.0.1:8082` respectively. (The binary accepts the port as its first command-line argument: `./tz-server <port>`).
3. Ensure the processes run with their timezone configured to `Europe/Berlin` using environment variables. The server will output the local time in its JSON response.

**Step 3: Fix the Monitor Script**
There is a monitor script at `/app/tz-server-1.0/monitor.sh` that simulates a cron job. It periodically checks the application and writes `OK` to a `health.status` file. 
1. Currently, due to path assumptions, it writes the file to whatever the current working directory is. Modify the script so it *always* writes the status to exactly `/home/user/data/health.status` regardless of where the script is executed from.
2. Create the `/home/user/data` directory.
3. Run the monitor script in the background.

**Step 4: Nginx Reverse Proxy**
Set up an Nginx reverse proxy to load balance incoming requests across the two microservice instances.
1. Create an Nginx configuration file at `/home/user/nginx.conf`.
2. Configure Nginx to run as a non-root user (store the PID file at `/home/user/nginx.pid` and ensure `error_log` and `access_log` point to `/home/user/data/` or `/dev/null`). Use `/home/user/data/client_temp` and similar paths for Nginx temp directories to avoid permission errors.
3. Nginx must listen on `127.0.0.1:8080`.
4. Route the endpoint `/time` to the upstream group containing `127.0.0.1:8081` and `127.0.0.1:8082`.
5. Route the endpoint `/health` to directly serve the `/home/user/data/health.status` file as text (using an `alias` or `root` directive combined with `try_files`).
6. Start Nginx in the background using your configuration file.

Ensure all services (both `tz-server` instances, the `monitor.sh` loop, and `nginx`) are running in the background when you complete your task.
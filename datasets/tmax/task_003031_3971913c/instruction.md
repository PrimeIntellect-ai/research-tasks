You are acting as a backup operator performing a routine restore test of our critical "LogAnalyzer" service. The restored stack is failing to serve traffic, and its performance is currently unacceptable. 

The environment is located in `/app/restore-env`, which contains a `docker-compose.yml` file defining three services:
1. `nginx`: The reverse proxy.
2. `go-app`: The main Go application that processes restored logs.
3. `ssh-bastion`: A simulated bastion host for administrative access.

Your tasks are:

1. **Mount Configuration**: We have a backup image located at `/app/backup.sqsh` (a squashfs archive). Since you do not have root access, you must mount this image to `/app/data` using `squashfuse`. Furthermore, append a valid fstab-like entry to `/app/restore-env/fstab` for documentation purposes (format: `/app/backup.sqsh /app/data squashfs defaults 0 0`). 

2. **Container Lifecycle & Nginx Fix**: Start the multi-service environment. You will notice that Nginx is currently returning a 502 Bad Gateway when you curl `http://localhost:8080` (mapped to port 80 in Nginx). Analyze `/app/restore-env/nginx/nginx.conf` and `/app/restore-env/go-app/main.go`. Nginx is configured to look for an upstream socket, but the Go app is listening on the wrong path or protocol. Fix the configurations so Nginx correctly routes requests to the Go app. Restart the necessary containers.

3. **Performance Optimization (Metric Threshold)**: The Go application exposes an endpoint at `http://localhost:8080/stats` which parses a massive text log file located in the mounted `/app/data/access.log`. Currently, the Go code uses an extremely inefficient text processing pipeline (re-compiling regular expressions inside a loop) which makes the request take several seconds. You must modify `/app/restore-env/go-app/main.go`, recompile it, and restart the `go-app` container so that the `/stats` endpoint consistently responds in **under 250 milliseconds**.

4. **SSH Tunneling**: The Go application also exposes an internal metrics endpoint on port `9090` (accessible only within the Docker network). Create a background SSH tunnel via the `ssh-bastion` service to forward your local machine's port `9090` to the `go-app` container's port `9090`. The bastion accepts SSH connections on `localhost:2222` with the user `admin` and password `adminpass`.

When you are finished, ensure the containers are running, the mount is active, the Nginx 502 is resolved, the endpoint is optimized, and the SSH tunnel is active. Create a file named `/app/done.txt` containing the word `SUCCESS` when you are ready for evaluation.
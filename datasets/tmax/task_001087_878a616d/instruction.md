You are an infrastructure engineer tasked with fixing and optimizing a deployment pipeline for a custom routing daemon. 

The system relies on a local Git repository for configuration management and deployment. Currently, the deployment is broken, the daemon fails to start due to network configuration issues, and the routing tables are highly unoptimized.

Your tasks are:

1. **Git Server & Hook Configuration**:
   A bare Git repository exists at `/home/user/router_deploy.git`. 
   You must create a `post-receive` hook in this repository that:
   - Checks out the main branch to `/home/user/deployed_router`.
   - Compiles a Go program named `optimizer.go` (which you will write and commit to the repo).
   - Executes the compiled `optimizer` to read `/home/user/raw_routes.txt` and generate `/home/user/deployed_router/routes.conf`.
   - Executes `/home/user/start_daemon.sh` to launch the daemon.

2. **Network Interface & Routing Configuration**:
   The daemon (`/app/router_daemon`) must run inside an isolated network namespace to prevent host conflicts, but the current startup script `/home/user/start_daemon.sh` is incomplete. 
   Modify `/home/user/start_daemon.sh` so that it:
   - Uses `unshare --net --user --map-root-user` to run the daemon.
   - Inside the namespace, creates a `dummy0` network interface.
   - Assigns the IP address `10.99.0.1/24` to `dummy0` and brings it `up`.
   - Adds a local route mapping `192.168.100.0/24` to the `dummy0` interface.
   - Starts `/app/router_daemon /home/user/deployed_router/routes.conf` inside that namespace in the background, writing its PID to `/home/user/daemon.pid`.

3. **Go Implementation (CIDR Optimization)**:
   The file `/home/user/raw_routes.txt` contains hundreds of overlapping IPv4 CIDR blocks (one per line). The daemon will crash or run inefficiently if the routing table is too large.
   Write `optimizer.go` (and commit it to the repo) to:
   - Read all CIDR blocks from `/home/user/raw_routes.txt`.
   - Perform optimal Route Summarization (CIDR aggregation). For example, `192.168.0.0/24` and `192.168.1.0/24` should be merged into `192.168.0.0/23`.
   - Write the minimized, non-overlapping list of CIDR blocks to `routes.conf` (one per line).

You will know you have succeeded when you push your code to `/home/user/router_deploy.git`, the `post-receive` hook successfully aggregates the routes into a minimal set, and the stripped binary daemon successfully starts and remains running in the network namespace.
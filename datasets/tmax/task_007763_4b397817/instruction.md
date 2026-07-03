You are a Cloud Architect managing the migration of a legacy network service to a new containerized infrastructure using a rolling deployment strategy. Since you do not have root access on this environment, you are simulating the deployment state using symbolic links and local processes.

Your objective is to build a custom C-based deployment monitor that performs health checks on a sequence of service endpoints, mimics an `fstab`-style mapping for the deployment targets, and manages a rolling upgrade by swapping the active "mount" (symbolic link) as newer versions become healthy.

Step 1: Create the Migration Configuration
Create a file at `/home/user/migration_fstab.txt` with the following contents. This file represents your deployment stages, mock mount paths, local TCP ports, and the expected startup delay (in seconds) for each mock container:
```text
service_v1 /home/user/deployments/v1 8001 0
service_v2 /home/user/deployments/v2 8002 3
service_v3 /home/user/deployments/v3 8003 6
```

Step 2: Create Mock Deployment Directories
Create the target directories specified in the config above (`/home/user/deployments/v1`, `/home/user/deployments/v2`, `/home/user/deployments/v3`). In each directory, create a simple text file named `info.txt` containing the name of the service (e.g., `service_v1`).

Step 3: Create the Mock Container Script
Write a bash script at `/home/user/start_mocks.sh` that reads `/home/user/migration_fstab.txt`. For each line, the script should wait in the background for the specified startup delay (the 4th column), and then start a local process that listens on the specified TCP port (the 3rd column). You can use `python3 -m http.server` or `nc` to mock the listening service.

Step 4: Write the Deployment Monitor in C
Write a C program at `/home/user/deploy_monitor.c` and compile it to `/home/user/deploy_monitor`. The program must:
1. Parse `/home/user/migration_fstab.txt`.
2. Enter a monitoring loop (polling every 1 second).
3. In each iteration, perform a TCP health check to `127.0.0.1` on the port of each configured service. A service is considered "Healthy" if a TCP connection is successfully established.
4. Implement a rolling deployment: Ensure that a symbolic link at `/home/user/live_service` points to the `TargetPath` (the 2nd column) of the *highest version* (the lowest on the list) service that is currently healthy. 
5. If a newer service becomes healthy, atomic-swap or update the symlink to point to the new service's directory. 
6. Every time a new version is successfully deployed (the symlink is updated), append a log entry to `/home/user/migration_events.log` with the exact format:
   `DEPLOYED <ServiceName> TO <TargetPath> ON PORT <Port>`
7. The program should exit cleanly once the final service (`service_v3`) has been deployed and logged.

Step 5: Execution
Run your bash script to start the mock services, then immediately run your C program. Ensure `/home/user/migration_events.log` contains the step-by-step history of your rolling deployment.
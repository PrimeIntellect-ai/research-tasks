You are a container specialist managing a suite of multi-language microservices. Recently, an update to the container provisioning system caused filesystem permission issues, preventing one of the services from starting correctly. 

You need to diagnose the environment using bash command-line tools.

Here is the current state of the system:
- Three microservices are configured to run locally: Python Service (`py-service` on port 8001), Node Service (`node-service` on port 8002), and Go Service (`go-service` on port 8003).
- Because of the failure, only two of these ports are currently accepting connections. The failing service's port is closed.
- You have a mock user account file at `/home/user/container_users.txt` that defines the expected User ID (UID) for each service. It follows the standard `/etc/passwd` format.
- Since you do not have root access to inspect the container layers directly, an automated tool has dumped the directory ownership metadata to `/home/user/fs_meta.txt`. Each line contains a service name and the actual UID assigned to its root directory, separated by a space.

Your task is to:
1. Perform connectivity diagnostics to determine which service's port is currently down.
2. Find the expected UID for that failing service from `/home/user/container_users.txt`.
3. Find the actual UID of that failing service's directory from `/home/user/fs_meta.txt`.
4. Create a diagnostic report at `/home/user/report.csv`. 

The file `/home/user/report.csv` must contain exactly one line with the following comma-separated values (no spaces):
`service_name,failing_port,expected_uid,actual_uid`

Use only standard bash utilities to complete this task.
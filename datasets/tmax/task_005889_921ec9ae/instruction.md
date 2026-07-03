You are a cloud architect migrating a legacy backend service to a new staged deployment environment. The legacy deployment script's token-based authentication is broken (it silently rejects CLI arguments) and now requires an interactive prompt, which breaks our CI/CD pipeline. 

Your task is to automate this interactive deployment, verify its health with a custom C++ monitor, and configure the correct file access control lists (ACLs) for the monitoring daemon.

Perform the following steps:

1. **Automate the Deployment**:
   Write an Expect script at `/home/user/auto_deploy.exp` that automates the execution of `/home/user/legacy_deploy.sh`. 
   The script will prompt with exactly: `Enter migration token: `
   Your expect script must automatically provide the token: `CloudMigrate2024!` and allow the deployment to finish. 
   Run your Expect script. A successful run will create `/home/user/deploy_dir/status.txt`.

2. **C++ Health Check**:
   Write a C++ program at `/home/user/health_check.cpp` and compile it to `/home/user/health_check`.
   This program must read the file `/home/user/deploy_dir/status.txt`. 
   If the first line of the file contains the exact string "READY", the C++ program must create/overwrite the file `/home/user/deploy_dir/health_log.txt` and write the exact string "HEALTHY" (followed by a newline) into it.
   Execute your compiled `/home/user/health_check` binary.

3. **Permission Management**:
   The monitoring service runs as the `daemon` user. Use Access Control Lists (ACLs) to specifically grant read permission (`r`) to the user `daemon` on the file `/home/user/deploy_dir/health_log.txt` without changing the file's standard Unix owner or group.

Ensure you execute the expect script, run the health check, and apply the ACLs before finishing the task.
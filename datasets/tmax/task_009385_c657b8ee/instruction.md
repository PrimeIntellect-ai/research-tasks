We are building a local mock Kubernetes operator testing environment. Due to a recent migration, our pipeline is broken. A legacy interactive tool blocks the pipeline, our mock operator fails to start due to dependency ordering issues, and our notification system is pointing to the wrong local port.

Your task is to fix the pipeline by writing an Expect script, configuring a Git hook, fixing the startup order of our local mock services, and setting up user-level port forwarding. 

You must complete the following steps in `/home/user`:

1. **Interactive Script Automation**: 
   There is an interactive script at `/home/user/bin/approve-manifests` that simulates a manual approval step. When executed, it prompts exactly with:
   `Enter operator password: ` (you should provide the password: `k8s-ops-secret`)
   `Confirm deployment (yes/no): ` (you should provide: `yes`)
   Write an Expect script at `/home/user/auto-approve.exp` that automatically runs `/home/user/bin/approve-manifests` and handles these prompts successfully. The script must return a 0 exit code on success.

2. **Port Forwarding**:
   Our mock notification service runs on `127.0.0.1:2525`. However, the mock applier is hardcoded to connect to `127.0.0.1:10025`. 
   Write a Bash script at `/home/user/port-forward.sh` that uses `socat` to forward TCP traffic from `127.0.0.1:10025` to `127.0.0.1:2525`. Run this script in the background so the forwarding is active.

3. **Git Hook & Operator Startup Fix**:
   We have a bare Git repository at `/home/user/manifests.git`. 
   Create a `post-receive` hook at `/home/user/manifests.git/hooks/post-receive`. Ensure it is executable.
   When triggered, the hook must perform the following actions in order:
   
   a. Check out the latest `master` branch to `/home/user/deploy-stage/` (create the directory if it doesn't exist).
   b. Execute your Expect script `/home/user/auto-approve.exp`. If it fails, the hook should exit.
   c. **Dependency Fix**: We have two mock operator scripts: `/home/user/bin/validator-daemon.sh` and `/home/user/bin/applier.sh`. `applier.sh` will crash if `validator-daemon.sh` is not already fully running and listening on port `8080`. 
      In the hook, start `/home/user/bin/validator-daemon.sh` in the background. Write a Bash polling loop that checks if `127.0.0.1:8080` is accepting TCP connections (you can use `nc` or `bash` `/dev/tcp`). Wait until the port is open before proceeding.
   d. Once port `8080` is open, execute `/home/user/bin/applier.sh /home/user/deploy-stage/`. This script processes the manifests and sends a notification via port `10025`.

Ensure all necessary scripts are executable. Do not use `sudo` or modify system-wide settings.
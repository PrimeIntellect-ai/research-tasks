You are a capacity planner building an automated deployment pipeline to fetch legacy resource usage metrics from a secure internal service. You need to set up a GitOps workflow where pushing a configuration triggers an isolated container to fetch and log the metrics.

Your task is to implement this pipeline entirely within `/home/user`. 

1. **Git Server & Hook Configuration**:
   - Initialize a bare Git repository at `/home/user/capacity_control.git`.
   - Create a `post-receive` hook in this repository. 
   - When code is pushed, the hook must extract the latest commit into `/home/user/capacity_workspace` and execute a script named `trigger_analysis.sh` located in the root of the pushed repository.

2. **SSH Tunneling & Port Forwarding**:
   - The legacy metric service is running on `localhost:8888`, but your analysis tools are configured to only talk to port `9999`.
   - Inside `trigger_analysis.sh`, establish a background SSH tunnel that forwards local port `9999` to `localhost:8888`. Use the current user (`user@localhost`) and standard SSH port 22. (Assume passwordless SSH access to `localhost` is already configured for the `user` account).

3. **Container Lifecycle Management**:
   - After the tunnel is up, `trigger_analysis.sh` must pull an Apptainer image (`docker://alpine:latest`) to `/home/user/alpine.sif`.
   - Start a background Apptainer instance named `metric_sandbox` using this image.
   - You must execute your metric fetching logic (see step 4) *inside* this running Apptainer instance.
   - Once the fetch is complete, the script must cleanly stop the Apptainer instance and terminate the SSH tunnel.

4. **Expect Scripting for Interactive Automation**:
   - The legacy service on port 8888 (now accessible via the tunnel on port 9999) is an interactive TCP service (not HTTP). 
   - When you connect to it (e.g., via `nc localhost 9999`), it prompts: `Login: `
   - You must send the username: `planner`
   - It will then prompt: `Password: `
   - You must send the password: `metrics_pass_99`
   - It will then output a JSON payload representing the capacity data and close the connection.
   - Write an Expect script (executed inside the `metric_sandbox` Apptainer instance) to automate this interaction. The Expect script must save the exact JSON payload returned by the service into `/home/user/capacity_report.json`.

**Testing your setup**:
You must leave the system in a state where if a user were to run the following commands:
```bash
cd /home/user
mkdir test_repo && cd test_repo
git init
git remote add origin /home/user/capacity_control.git
# ... (user adds trigger_analysis.sh and expect scripts) ...
git add . && git commit -m "Deploy analysis"
git push origin master
```
The result would be the successful execution of the hook, tunnel, container, and expect script, culminating in the creation of `/home/user/capacity_report.json` containing the metrics data. You do *not* need to perform the push yourself; just ensure the repository, hook, and your prepared scripts in the workspace are ready to handle it. You should write the `trigger_analysis.sh` and Expect scripts and place them in a folder `/home/user/repo_contents` so an automated test can commit and push them to verify your pipeline.
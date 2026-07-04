You are an infrastructure engineer tasked with automating the provisioning of network routing nodes. You must wrap a legacy, interactive provisioning utility into a fully automated, background-running system. 

There is a legacy Python script located at `/home/user/legacy_net_setup.py`. We cannot modify this script. When executed, it interactively prompts the user for three configuration values sequentially:
1. `Enter cluster name:`
2. `Enter base port (1024-65535):`
3. `Enable IPv6? (y/n):`

After receiving the third input, the script processes them and outputs a multi-line report to standard output. The last line of the output is always in the format:
`SUCCESS: Node configured. token=<encoded_string> endpoint=<ip>:<port>`

Your task is to build an automation pipeline that interacts with this script and extracts the required data:

1. **Interactive Automation (`/home/user/auto_provision_runner`)**:
   Write a script (in any language of your choice, such as Python or bash+expect) that programmatically executes `/home/user/legacy_net_setup.py`. It must automatically answer the prompts using values provided to it. 
   - It should read the cluster name from an environment variable `$CLUSTER_NAME`.
   - It should read the base port from an environment variable `$BASE_PORT`.
   - It should always answer `n` for the IPv6 prompt.

2. **Text Processing Pipeline**:
   The `auto_provision_runner` must parse the output of the legacy script. It must extract *only* the `<encoded_string>` value (the value of `token=`) from the final SUCCESS line and output only that token string to standard output.

3. **Service Lifecycle Management (`/home/user/provision_daemon.sh`)**:
   Create a bash script that acts as a background daemon. When run, it should continuously loop (e.g., polling every 1 second). 
   - It must check for the existence of a trigger file at `/home/user/job_queue.txt`.
   - If the file exists, it should source the environment variables defined inside it (the file will contain lines like `export CLUSTER_NAME=XYZ` and `export BASE_PORT=1234`).
   - After loading the variables, it must execute `/home/user/auto_provision_runner`.
   - It must append the generated token (the output of the runner) to `/home/user/processed_tokens.log`.
   - Finally, it must delete `/home/user/job_queue.txt` and resume polling.

4. **Environment & Execution**:
   - Ensure all scripts are executable (`chmod +x`).
   - Start your daemon running in the background (e.g., using `nohup /home/user/provision_daemon.sh &`).
   - Leave the daemon running so that automated tests can drop `job_queue.txt` files and observe `/home/user/processed_tokens.log`.
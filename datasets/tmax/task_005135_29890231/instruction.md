You are a deployment engineer tasked with creating an automated rollout tool for virtualized applications. Your team uses QEMU to run application virtual machines and connects to them via VNC. 

You need to write a Python script at `/home/user/deploy_vm.py` that automates the deployment directory structuring, QEMU script generation, and logging. 

Before you start, assume there is a base image located at `/home/user/images/base.img`. (You may need to create this directory and a dummy file to test your script).

Your Python script `/home/user/deploy_vm.py` must accept two command-line arguments using the `argparse` module:
* `--version`: An integer representing the version number being deployed.
* `--vnc-port`: An integer representing the VNC display port to be used by QEMU.

When executed, the script must perform the following actions:
1. **Directory and Link Management:**
   * Create a deployment directory at `/home/user/deployments/v<version>` (create parent directories if they don't exist).
   * Create a symbolic link at `/home/user/deployments/v<version>/disk.img` that points to `/home/user/images/base.img`.
   * Create or update a symbolic link at `/home/user/deployments/current` so that it points to the directory `/home/user/deployments/v<version>`.

2. **QEMU Script Construction:**
   * Create a bash script at `/home/user/deployments/v<version>/run.sh`.
   * The script must be executable (e.g., `chmod +x`).
   * The contents of the script must be exactly:
     ```bash
     #!/bin/bash
     qemu-system-x86_64 -m 1024 -drive file=disk.img,format=qcow2 -vnc :<vnc-port>
     ```
     (Replacing `<vnc-port>` with the actual provided argument).

3. **Log Configuration and Rotation:**
   * Configure Python's standard `logging` module to write to `/home/user/deployments/deploy.log`.
   * You must use a `RotatingFileHandler` with `maxBytes=500` and `backupCount=2`.
   * The log format must be exactly: `%(levelname)s - %(message)s`
   * First, log the following message at the INFO level:
     `Deployed version <version> on VNC port <vnc-port>`
   * Next, to ensure log rotation is working, write a loop that executes 20 times (from 1 to 20 inclusive), logging this exact message at the INFO level on each iteration:
     `Padding log line <iteration_number> for rotation testing`

Once your script is written, execute it with `--version 42` and `--vnc-port 5` to perform the deployment. Ensure all directories, symlinks, scripts, and rotated logs are generated successfully.
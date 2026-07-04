You are a deployment engineer tasked with rolling out an automated local update pipeline using Git, Podman, and user-level systemd. Since you do not have root access, you will be configuring user-level services and simulated configuration files.

Please complete the following tasks:

1. **Storage Configuration (Simulated fstab):**
   Create a file at `/home/user/app_storage.fstab`. Inside it, write exactly one valid `fstab` line that mounts a filesystem with UUID `9b1c990b-8f19-4b6d-9799-a3b043b177d4` to the directory `/home/user/app_data` using the `ext4` filesystem. Use the mount options `defaults,nofail` and set the dump and pass numbers to `0` and `2` respectively.
   (Also, ensure the directory `/home/user/app_data` actually exists).

2. **Git Server and Hook:**
   Create a bare Git repository at `/home/user/deploy.git`.
   Configure a `post-receive` hook inside this bare repository. The hook must:
   - Check out the latest code from the `main` branch into the working tree directory `/home/user/app_src` (create this directory).
   - Restart a user-level systemd service named `app-worker.service`.

3. **Container Lifecycle & Process Supervision:**
   Create a user-level systemd unit file at `/home/user/.config/systemd/user/app-worker.service`.
   The service should:
   - Run a container using `podman` with the `python:3.10-alpine` image.
   - Name the container `app-worker` and ensure it replaces any existing container with the same name (`--replace` flag or `rm` in ExecStartPre).
   - Bind mount `/home/user/app_src` to `/app` inside the container.
   - Bind mount `/home/user/app_data` to `/data` inside the container.
   - Set the working directory inside the container to `/app`.
   - Execute the command: `python /app/main.py`.
   - Have a restart policy of `Restart=on-failure`.

   Enable and start this systemd service (it will likely fail initially since `main.py` is not there yet, which is fine).

4. **Trigger the Pipeline:**
   Clone the bare repository to `/home/user/workspace`.
   Inside the workspace, create a `main.py` file with the following Python code:
   ```python
   import time

   with open("/data/deploy_log.txt", "a") as f:
       f.write("Update deployed successfully\n")

   print("Application running...")
   time.sleep(3600)
   ```
   Commit this file to the `main` branch and push it to the bare repository at `/home/user/deploy.git`.

By pushing the code, your Git hook should fire, checking out the code and restarting the `app-worker` service. The podman container will run the new Python script, which will write to the mounted data volume.

Verify your setup by ensuring that `/home/user/app_data/deploy_log.txt` exists and contains "Update deployed successfully".
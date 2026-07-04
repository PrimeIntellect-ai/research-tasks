You are tasked with building a custom, lightweight "operator" that manages Virtual Machine deployments via mock QEMU commands, simulating a Kubernetes-like reconciliation loop. You will implement this using Python and standard Bash tooling. 

You must create a CI/CD pipeline script, a backup mechanism, and an idempotent Python operator script. 

The system operates on manifest files defining VMs. Two manifest files already exist:
`/home/user/manifests/web.json`
`/home/user/manifests/db.json`

Your task consists of the following phases:

**Phase 1: Directory Setup & Backup Strategy**
1. Create the following directories if they don't exist:
   - `/home/user/deployments`
   - `/home/user/state`
   - `/home/user/backups`
2. Write a bash script at `/home/user/backup.sh` that creates a compressed tarball of the `/home/user/state` directory and saves it to `/home/user/backups/state_backup.tar.gz`. The script should create the tarball directly without any intermediate files.

**Phase 2: The Operator (Python)**
Write a Python script at `/home/user/operator.py` that acts as the reconciliation loop.
1. The script must iterate over all `.json` files in `/home/user/manifests/`.
2. Each JSON manifest contains the following structure:
   `{"metadata": {"name": "<vm_name>"}, "spec": {"qemu_image": "<path>", "vnc_port": <port_number>, "memory": "<memory_string>"}}`
3. **Idempotency:** For each manifest, check if a corresponding state file exists at `/home/user/state/<vm_name>.json`. 
   - If the state file exists AND its last modification time (`mtime`) is strictly greater than or equal to the manifest's `mtime`, skip processing this manifest.
4. If it needs processing, the operator must:
   - Generate an executable bash script at `/home/user/deployments/launch_<vm_name>.sh`. The script must contain exactly these two lines:
     `#!/bin/bash`
     `qemu-system-x86_64 -m <memory> -hda <qemu_image> -vnc 127.0.0.1:<vnc_port> -daemonize`
     (Replace the placeholders with the actual values from the JSON manifest).
   - Generate a state file at `/home/user/state/<vm_name>.json` containing exactly this JSON structure:
     `{"status": "deployed", "name": "<vm_name>", "port": <vnc_port>}`

**Phase 3: The CI/CD Pipeline**
Write a bash script at `/home/user/pipeline.sh` that ties it all together:
1. First, it must execute `/home/user/backup.sh`.
2. Next, it must execute `python3 /home/user/operator.py`.
3. Then, it must perform a syntax check on all generated launch scripts using `bash -n /home/user/deployments/launch_*.sh`.
4. Finally, if all previous commands succeed, append the exact string `PIPELINE SUCCESS` to `/home/user/pipeline.log`.

Make sure `/home/user/backup.sh` and `/home/user/pipeline.sh` are executable. Do not run the pipeline script yourself; the automated verification system will run `/home/user/pipeline.sh` to test your solution.
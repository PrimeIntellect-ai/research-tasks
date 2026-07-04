You are an infrastructure engineer automating the provisioning and CI/CD pipeline for a lightweight C++ monitoring agent. The agent is responsible for validating custom mount configurations and checking network connectivity to a specific backend service.

Your task is to implement the monitor, its containerization instructions, and a CI script that provisions and tests it locally. All files must be created within `/home/user/project` (create the directory).

Step 1: Mount Configuration
Create a mock fstab file at `/home/user/fstab.conf` containing exactly this line:
`/dev/mapper/data_vol /home/user/mnt/data ext4 defaults 0 0`

Step 2: C++ Monitoring Agent
Create a C++ program at `/home/user/project/nas_monitor.cpp`. The program must do the following:
1. Parse `/home/user/fstab.conf` to extract the mount point associated with `/dev/mapper/data_vol`.
2. Ensure the extracted mount point directory (`/home/user/mnt/data`) exists (create the directories if they do not exist).
3. Attempt to establish a TCP connection to `127.0.0.1` on port `8080`.
4. Write a JSON result to `/home/user/project/monitor.json` strictly in this format:
`{"mount_target": "<extracted_path>", "network_ok": <true/false>}`

Step 3: Containerization Definition
Write a `Dockerfile` at `/home/user/project/Dockerfile` that:
- Uses `ubuntu:22.04` as the base image.
- Installs `g++` and `make`.
- Copies `nas_monitor.cpp` into `/app/`.
- Compiles the C++ file to `/usr/local/bin/nas_monitor`.
- Sets the default entrypoint to run the compiled binary.

Step 4: CI/CD Pipeline Script
Write a bash script at `/home/user/project/ci.sh` (make it executable) that orchestrates the local testing:
1. Starts a background Python dummy server on port `8080` (e.g., using `python3 -m http.server 8080`) to satisfy the network check. Give it a second to start.
2. Compiles `nas_monitor.cpp` locally using `g++` to create `/home/user/project/nas_monitor`.
3. Runs the compiled `nas_monitor` binary.
4. Cleans up (kills) the background Python server after the C++ binary finishes executing.

Finally, execute your `/home/user/project/ci.sh` script to perform the end-to-end run. Leave the generated `/home/user/project/monitor.json` in place for verification.
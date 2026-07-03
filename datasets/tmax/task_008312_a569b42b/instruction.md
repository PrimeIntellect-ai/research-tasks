You are a site administrator responsible for managing user accounts and their isolated data-processing environments. Due to a previous network misconfiguration, users cannot directly reach the central data processing service on port 9999. You need to provision their directories and generate a script that establishes port forwarding for each user.

Your task is to write a Rust application that automates the provisioning of user workspaces and generates an idempotent network configuration script.

1. Create a new Rust project using Cargo at `/home/user/account_provisioner`.
2. Your Rust program must read a CSV file located at `/home/user/accounts.csv`. The CSV has no header and contains rows in the format: `username,port_offset` (e.g., `alice,15`).
3. For each user in the CSV, your Rust program must perform the following filesystem operations idempotently (it should succeed without modifying existing correct states if run multiple times):
    * Create the directory structure: `/home/user/workspaces/<username>/logs` and `/home/user/workspaces/<username>/data`.
    * Ensure an empty file exists at `/home/user/workspaces/<username>/logs/latest.log`.
    * Create a relative symbolic link at `/home/user/workspaces/<username>/active_log` that points to `logs/latest.log`.
4. Your Rust program must also generate a Bash script at `/home/user/workspaces/setup_tunnels.sh`. 
    * For each user, the script should establish a port forward using `socat` from a local port (`8000 + port_offset`) to `127.0.0.1:9999`.
    * The script MUST be idempotent. For each user, it should first check if the target local port (e.g., 8015) is already in use. If it is not in use, it should execute: `socat TCP-LISTEN:<port>,fork,bind=127.0.0.1 TCP:127.0.0.1:9999 &`
    * Make sure the generated script has executable permissions (`0755`).
5. Build and run your Rust application so that the `/home/user/workspaces/` directory is fully populated and the script is generated.
6. Execute the generated `/home/user/workspaces/setup_tunnels.sh` script to simulate the environment startup. 

Do not install any global system packages requiring root; `socat` and `cargo` are already available.
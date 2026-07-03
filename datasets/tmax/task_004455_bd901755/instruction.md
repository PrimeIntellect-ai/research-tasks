You are a capacity planner building a custom storage monitoring pipeline for a simulated environment. You need to write a metric exporter in Rust, an idempotent environment setup script, and the necessary systemd configurations to manage the service lifecycle.

Since you do not have root access in this environment, you will create user-level mock directories and configuration files.

Perform the following tasks:

1. **Idempotent Setup Script**:
   Create a bash script at `/home/user/init_mount.sh`. This script must:
   - Make it executable.
   - Idempotently create the directory `/home/user/mock_mount` (it should not fail if the directory already exists).
   - Idempotently create a file named `data.bin` inside `/home/user/mock_mount` that is exactly 4096 bytes in size (filled with zero bytes). If the file already exists and is 4096 bytes, do nothing.
   - Be completely self-contained and safe to run multiple times without causing errors or changing the final expected state.

2. **Mock fstab Configuration**:
   Create a file at `/home/user/custom_fstab` that simulates an fstab entry for your mount point. It must contain exactly this single line:
   `/dev/loop0 /home/user/mock_mount ext4 defaults 0 0`

3. **Rust Metric Exporter**:
   Create a new Rust Cargo project at `/home/user/capacity_monitor`. 
   Write a Rust application that:
   - Listens for raw TCP connections on `127.0.0.1:9090`.
   - When a client connects, the server must calculate the total size (in bytes) of all files directly inside `/home/user/mock_mount` (you only need to check the files directly in this directory, no recursive traversal is strictly required for this test).
   - Sends the response to the connected client in exactly this format: `BYTES:<total_size>\n` (e.g., `BYTES:4096\n`).
   - Closes the connection immediately after sending the data.
   - Runs continuously serving multiple sequential requests.
   - Build your project in release mode (`cargo build --release`) so the binary exists at `/home/user/capacity_monitor/target/release/capacity_monitor`.

4. **Systemd Service Configuration**:
   Create a systemd unit file at `/home/user/capacity-exporter.service`.
   - The `[Service]` section must define `ExecStart` pointing to your compiled Rust binary: `/home/user/capacity_monitor/target/release/capacity_monitor`.
   - To ensure the exporter doesn't start before the network and the mock storage mount are ready, the `[Unit]` section must include an `After=` directive that specifies both `network-online.target` and a custom service named `mount-prep.service`.
   - Include a basic `[Install]` section with `WantedBy=default.target`.

Ensure all files are created at the exact absolute paths specified above. Do not start the Rust service manually blocking the terminal; the automated tests will compile/run your code and inspect your configuration files directly.
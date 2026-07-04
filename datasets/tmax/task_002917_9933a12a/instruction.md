You are an edge computing engineer deploying a new data pipeline to our IoT devices. We are migrating away from a legacy proprietary sensor processing daemon.

You have several distinct objectives to prepare the edge environment and port the legacy logic.

1. **Environment Setup:**
   - Create a 10MB ext4 filesystem image at `/home/user/data.img`.
   - Create a mount point directory at `/home/user/data_mount`.
   - Create a file `/home/user/fstab_entry` containing the exact line you would add to `/etc/fstab` to mount this image at `/home/user/data_mount` using the `ext4` filesystem with default options (assume loop mount).
   - We need the timezone set for our Berlin deployments. Create a file `/home/user/sensor_env.sh` that exports the `TZ` environment variable set to `Europe/Berlin` and sets `LANG` to `en_US.UTF-8`.

2. **Port Forwarding:**
   - Our control plane expects telemetry on port 8080. Create a background SSH tunnel that forwards local port 8080 to `localhost:9090` (assume you can SSH into `localhost` as `user` with no password or using your existing keys). Write the SSH command you used to `/home/user/ssh_tunnel_cmd.txt`.

3. **Legacy Binary Automation (Expect):**
   - The old daemon is located at `/app/legacy_sensor_bin`. If you run `/app/legacy_sensor_bin --setup`, it interactively asks two questions:
     - "Initialize sensor storage? (yes/no):" -> You must answer `yes`
     - "Enter Site ID:" -> You must answer `EDGE-99`
   - Write an Expect script at `/home/user/automate_setup.exp` that spawns this command and automatically answers these prompts.

4. **Logic Porting (The Core Task):**
   - The file `/app/legacy_sensor_bin` is a stripped binary. When run normally (without `--setup`), it reads exactly one line of text from standard input, applies a specific data transformation, and prints the result to standard output.
   - You must reverse-engineer this black-box transformation by testing it with various inputs.
   - Once you understand the transformation, write a replacement program at `/home/user/process_sensor`. It can be a bash script, Python script, or compiled binary (make sure it is executable).
   - Your replacement must be BIT-EXACT equivalent to the legacy binary's output for any single-line printable ASCII input. It should not prompt for anything, just read from standard input, transform, and print to standard output.

Ensure all files are created exactly at the specified paths.
You are an edge computing engineer deploying operating systems to a batch of headless IoT devices. These devices are initialized via a simulated serial console interface that asks a series of interactive configuration questions. 

You must write a Rust application that automates this interactive provisioning step and generates the corresponding network configuration files.

**System Environment & Provided Files:**
- An interactive initialization script is located at `/home/user/qemu_serial_mock.sh`. This script simulates the serial console prompt of the IoT device. It prints questions to `stdout` and waits for input on `stdin`.
- A specification file for the device is located at `/home/user/deploy_spec.txt`. It contains four lines representing the desired configuration:
  1. Timezone (e.g., `Asia/Tokyo`)
  2. Locale (e.g., `ja_JP.UTF-8`)
  3. Interface IP with CIDR (e.g., `10.99.0.45/24`)
  4. Default Gateway (e.g., `10.99.0.1`)

**Your Objectives:**
1. Initialize a new Rust project at `/home/user/automator`.
2. Write a Rust program in this project that:
   - Reads the parameters from `/home/user/deploy_spec.txt`.
   - Spawns the `/home/user/qemu_serial_mock.sh` script as a child process.
   - Programmatically interacts with the process, feeding it the correct parameters in the order requested by the script. (The script will prompt for Timezone, Locale, IP, and Gateway sequentially).
   - Waits for the script to exit successfully.
3. After the interaction, your Rust program must generate a static routing configuration file at `/home/user/route-eth0.conf`. This file must contain exactly one line defining the default route using the gateway IP from `deploy_spec.txt`, formatted exactly as:
   `default via <GATEWAY_IP> dev eth0`

**Success Criteria:**
- The Rust project must compile successfully with `cargo build`.
- When your compiled Rust program is executed, it must successfully drive `/home/user/qemu_serial_mock.sh` to completion.
- Running the Rust program must result in the creation of `/home/user/vm_state.conf` (which is created internally by the mock script when completed successfully).
- The file `/home/user/route-eth0.conf` must be created by your Rust program with the exact format specified above.

Note: You do not have `sudo` privileges, and all work should be contained within `/home/user/`. Do not modify `/home/user/qemu_serial_mock.sh` or `/home/user/deploy_spec.txt`. Ensure your Rust application cleanly flushes standard I/O to avoid deadlocks.
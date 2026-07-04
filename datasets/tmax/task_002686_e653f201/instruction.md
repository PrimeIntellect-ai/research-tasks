You are an edge computing engineer preparing a configuration package for a new fleet of IoT gateway devices. These devices act as a bridge between isolated local IoT sensors and a central server, but they currently suffer from network misconfigurations preventing the services from communicating.

Since you are preparing this offline, you do not need to execute the network configuration commands as root. Instead, you must build the deployment package and scripts with the exact specifications required by the automated provisioning system.

Perform the following tasks:

1. **Filesystem Preparation**:
   Create a base deployment directory at `/home/user/edge_package`.
   Inside it, create two subdirectories: `data` and `keys`.
   Ensure the `data` directory has permissions `700` (read/write/execute for the owner only) to protect sensitive telemetry.

2. **User Authentication (SSH)**:
   Generate an ED25519 SSH key pair without a passphrase. Save the private key exactly to `/home/user/edge_package/keys/iot_key`. The public key should naturally be created alongside it.

3. **Network Configuration Script**:
   Create a bash script at `/home/user/edge_package/network_setup.sh`. This script will be run by the provisioner (which has root access). It must contain exactly two `ip` commands to:
   - Add a new dummy network interface named `sensor-net`.
   - Assign the IP address `192.168.100.1/24` to the `sensor-net` interface.
   Make sure `network_setup.sh` is executable.

4. **SSH Tunneling Script**:
   Create a bash script at `/home/user/edge_package/tunnel.sh`. This script should contain the exact `ssh` command to create a background local port forward.
   - It must bind the local device's port `8080`.
   - It must forward traffic to port `9000` on a target device with the IP `192.168.100.5`.
   - It must authenticate as the user `sensor_user` using the SSH key you generated (`/home/user/edge_package/keys/iot_key`).
   - It must run in the background without executing remote commands (use standard SSH flags for backgrounding and no-command).
   Make sure `tunnel.sh` is executable.

5. **Multi-language Aggregator**:
   Write a small Python 3 script at `/home/user/edge_package/verify_data.py`. The script must simply read a JSON string from standard input, parse it, and print the value of the key `"status"`. If the key doesn't exist, it should print `"unknown"`. Make this script executable.

Ensure all file paths, names, and permissions match these instructions exactly. Do not attempt to run the `network_setup.sh` script, just create it.
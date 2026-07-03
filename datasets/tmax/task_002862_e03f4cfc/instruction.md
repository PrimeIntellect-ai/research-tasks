You are an edge computing engineer deploying simulated IoT nodes for a smart factory. Your edge nodes are isolated in lightweight VMs and have a network misconfiguration preventing them from natively routing traffic back to the host machine where the provisioning API lives.

To bridge this gap, you need to configure the VM's network using QEMU port forwarding and establish an SSH reverse tunnel so the edge application can reach the host API.

Write the following scripts in `/home/user` to accomplish this end-to-end deployment setup. Do not execute the scripts; an automated testing suite will inspect them.

**1. The Host Provisioning API**
Write a Python script `/home/user/init_api.py` that:
- Uses the standard library `http.server` to start an HTTP server on port `8080` bound to `127.0.0.1`.
- It should serve files from the `/home/user/api_data` directory.

**2. The VM Launch Script**
Write a bash script `/home/user/launch_node.sh` that executes the `qemu-system-aarch64` command to boot an IoT image (`/opt/iot_image.img`). Include the following specific QEMU arguments:
- Machine type: `virt`
- Memory: `512M`
- Drive: file=/opt/iot_image.img,format=qcow2
- Display: VNC on display `:5`
- Networking: Configure user-mode networking (`-netdev user`) with hostfwd to map the host's port `2222` to the guest's port `22` (SSH). Bind the netdev to a NIC (`-device virtio-net-pci`).

**3. The SSH Tunneling Script**
Write a bash script `/home/user/establish_tunnel.sh` that constructs an `ssh` command to create a reverse tunnel.
- The tunnel must forward traffic from port `9090` on the guest VM to port `8080` on the host (localhost).
- The SSH connection must target the guest via the forwarded host port `2222` (i.e., connecting to localhost).
- Use the username `iotuser`.
- Ensure the tunnel command runs in the background, does not execute a remote command (`-N -f`), and bypasses host key checking (`-o StrictHostKeyChecking=no`).

**4. The Edge Client Payload**
Write a Python script `/home/user/edge_client.py` meant to be run inside the guest VM. It should:
- Use `urllib.request` to perform an HTTP GET request to `http://127.0.0.1:9090/config.json`.
- Save the downloaded content to `/tmp/local_config.json`.

Ensure all files have executable permissions where appropriate and strictly follow the path names specified.
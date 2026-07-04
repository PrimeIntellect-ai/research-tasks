You are an edge computing engineer deploying a new data collection service to a remote IoT node. The node has strict security boundaries and requires interactive provisioning. You need to automate the provisioning, write and deploy the C++ collection service, set up port forwarding, and configure the correct Access Control Lists (ACLs) for the collected data.

Perform the following steps:

1. **Automate Provisioning with Expect:**
   There is an interactive provisioning script located at `/home/user/iot_provision.sh`. When run, it prompts for a "Device ID" and a "Provisioning PIN".
   Write an `expect` script at `/home/user/provision.exp` to automate this. 
   - Send Device ID: `edge-node-99`
   - Send PIN: `4921`
   Run your expect script. If successful, it will generate a configuration file at `/home/user/device.conf`.

2. **Develop the C++ Edge Service:**
   Write a C++ program at `/home/user/edge_server.cpp` that acts as a simple TCP server.
   - It must listen on `127.0.0.1` port `8080`.
   - When a client connects and sends a text payload (up to 1024 bytes), the server must append the received payload to the file `/home/user/data/payload.log` followed by a newline, and then close the connection.
   - Compile this program to `/home/user/edge_server` using `g++` and start it in the background.

3. **Configure Port Forwarding:**
   The external sensors cannot reach port 8080 directly. Use `socat` to set up port forwarding so that any TCP traffic arriving on port `9090` is forwarded to `127.0.0.1:8080`. Start this `socat` process in the background.

4. **Manage Permissions and ACLs:**
   The data file `/home/user/data/payload.log` must be highly restricted but readable by a local analytics user named `guest`.
   - First, create the file `/home/user/data/payload.log` if your C++ program hasn't already.
   - Set the base permissions of `/home/user/data/payload.log` to `600` (read/write for the owner `user` only).
   - Use `setfacl` to grant the user `guest` explicit read-only (`r--`) access to `/home/user/data/payload.log`.

Verify your deployment by sending a test message to port `9090` (e.g., using `echo "TEST" | nc localhost 9090`) and ensuring it appears in the log file, and that the ACLs are correctly applied. Leave the background processes running.
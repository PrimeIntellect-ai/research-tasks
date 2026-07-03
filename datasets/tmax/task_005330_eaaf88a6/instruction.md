You are an edge computing engineer preparing an over-the-air (OTA) deployment package for a fleet of IoT gateway devices. The gateway runs a lightweight Linux OS and uses a custom C++ data aggregator to process sensor telemetry.

Your objective is to finalize the OTA payload and prepare the custom C++ aggregator tool.

**Step 1: Fix and Compile the Edge Aggregator**
We vendor the source code for our custom telemetry processor at `/app/edge-aggregator-1.0`. 
Currently, the `Makefile` is misconfigured. It fails to compile because it uses an older C++ standard, and it is running too slowly in production.
- Identify and fix the perturbation in `/app/edge-aggregator-1.0/Makefile`.
- Ensure it is compiled with modern C++ (C++17) and heavy optimization (`-O3`) so that it can meet strict latency requirements.
- Compile the binary to `/home/user/edge-aggregator`.

**Step 2: Edge Storage Configuration (fstab & quotas)**
The IoT device needs a dedicated storage partition for sensor data with disk quotas enabled to prevent runaway logs from crashing the system.
- Edit the OTA mock configuration file located at `/home/user/ota_payload/etc/fstab`.
- Add an entry to mount the block device `/dev/mmcblk0p3` to the mount point `/var/spool/iot_data`.
- Use the `ext4` filesystem.
- Include the mount options `defaults` and `usrquota`.

**Step 3: Network Forwarding (iptables)**
Sensor nodes send data to the gateway on port 80 (TCP), but the `edge-aggregator` daemon will run as a non-root user on port 8080.
- Create an iptables rules file at `/home/user/ota_payload/etc/iptables.rules`.
- Include the exact `iptables` command (or rule format) required to append a rule to the `nat` table's `PREROUTING` chain that redirects incoming TCP traffic on port 80 to port 8080. 
*(Write this file as a shell script format, e.g., starting with `iptables -t nat ...`)*

**Step 4: Metric Verification**
Run your compiled aggregator on the sample data to ensure it works:
`/home/user/edge-aggregator /app/sample_sensors.csv /home/user/ota_payload/test_output.bin`
The aggregator's performance will be evaluated against a hidden, massive dataset. Your compiled binary must process the data in under **1.5 seconds**.
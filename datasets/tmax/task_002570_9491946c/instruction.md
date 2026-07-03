You are a Site Reliability Engineer (SRE) debugging an automated uptime reporting pipeline. Due to lack of root access on this jumpbox, our team simulates mount points using a mock fstab and relies on local Git pushes to trigger uptime analysis.

Your objective is to fix the reporting pipeline by creating a C++-based Git hook, reading our configuration files, and setting up an SSH tunnel for our dashboard.

Follow these instructions exactly:

1. **Git Server & Hook (C++)**:
   - A bare Git repository exists at `/home/user/uptime.git`.
   - Write a C++ program at `/home/user/post_receive.cpp` and compile it to `/home/user/uptime.git/hooks/post-receive` (ensure it is executable).
   - The hook must read a file located at `/home/user/workspace/heartbeat.log` (assume the system extracts pushed files here before the hook runs, for simplicity).
   - The `heartbeat.log` contains lines of text, each with a timestamp and a status: `TIMESTAMP STATUS` (e.g., `1700000000 UP` or `1700000060 DOWN`).
   - The hook must calculate the uptime percentage as: `(Number of UP lines / Total lines) * 100`, truncated to an integer (floor).

2. **Mount/fstab Configuration Parsing**:
   - The C++ hook must read `/home/user/fstab.mock`. This file follows standard `fstab` syntax (`device mountpoint fstype options dump pass`).
   - The hook must find the line where the device is `/dev/mapper/uptime_data`.
   - Extract the `mountpoint` path from that line.
   - The hook must write the calculated uptime to a file named `latest.txt` inside that extracted mountpoint directory.
   - The output file (`latest.txt`) must contain exactly: `Uptime: <percentage>%` (e.g., `Uptime: 85%`).

3. **SSH Tunneling**:
   - We run a local dashboard server on port `8000`. You need to expose this via an SSH tunnel.
   - Create a script at `/home/user/setup_tunnel.sh` that, when run, uses `ssh` to set up local port forwarding.
   - It should forward local port `9999` to `localhost:8000`.
   - Use `ssh -N -f -L 9999:localhost:8000 user@localhost` (assume SSH keys are already configured for passwordless login to `localhost`).

Ensure your C++ code compiles without errors using `g++ -std=c++17`.
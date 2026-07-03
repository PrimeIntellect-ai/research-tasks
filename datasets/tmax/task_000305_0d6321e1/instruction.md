You are an edge computing engineer deploying an offline alerting system to an IoT device. The deployment package has several configuration and lifecycle management issues that prevent the edge services from communicating and starting correctly.

Your objective is to fix the configurations and write a robust startup script. 

All work must be done within `/home/user/`.

**Phase 1: Fix Storage Configuration**
The device image builder relies on a custom fstab file at `/home/user/system/fstab.iot`. It currently contains an invalid entry for the local data storage.
Fix the file so that the directory `/home/user/iot_storage` is mounted to `/mnt/iot_data` using the `bind` filesystem type. The options should be `defaults,bind`, dump should be `0`, and pass should be `0`. Ensure the spacing and standard fstab format is correct.

**Phase 2: Fix Network & Email Configuration**
The IoT sensor application needs to send alerts to a local edge-based SMTP service, but the network is misconfigured (simulating an isolated container network issue).
Edit `/home/user/config/mail.conf`. Change the `SMTP_HOST` and `SMTP_PORT` to route to the local loopback (`127.0.0.1`) on port `2525`, because the edge SMTP daemon is configured to listen locally to avoid exposing unauthenticated mail services on the external network interface.

**Phase 3: Robust Lifecycle Management Script**
Write a Bash script at `/home/user/start_iot.sh` that manages the lifecycle of the IoT processes (acting as a lightweight container manager).
The script MUST:
1. Start with robust error handling (`set -e` and `set -u`).
2. Read `/home/user/system/fstab.iot` and verify that the string `bind` is present. If not, exit with code 1.
3. Start the mock SMTP server by executing `python3 /home/user/bin/smtp_edge.py` in the background.
4. Start the sensor application by executing `bash /home/user/bin/sensor_app.sh` in the background.
5. Implement a robust `trap` on `SIGINT` and `SIGTERM`. When the script receives these signals, it must gracefully terminate (using `kill`) the backgrounded SMTP and sensor processes, and print exactly "CLEANUP_SUCCESS" to stdout before exiting.
6. Use the `wait` command to block and wait for both background processes to finish.

Make sure `/home/user/start_iot.sh` is executable.

The automated verification will:
1. Inspect your fixed `/home/user/system/fstab.iot` and `/home/user/config/mail.conf`.
2. Execute your `/home/user/start_iot.sh` script in the background.
3. Send a test signal to verify the processes started and can communicate.
4. Send a SIGTERM to your script to verify the trap cleanup correctly executes and shuts down the child processes.
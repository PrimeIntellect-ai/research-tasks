You are an edge computing engineer preparing a deployment and monitoring package for a new batch of resource-constrained IoT devices. Because you are working in an unprivileged build environment, you must script the necessary administrative commands to be run later by the deployment pipeline, as well as write the data-processing agent.

Your objective is to complete the following two tasks:

**1. Go Monitoring Agent**
The IoT devices report their storage via a simple text file located at `/home/user/device_storage.txt`. 
Write a Go program at `/home/user/monitor.go` that reads this file. The file will contain exactly one line in the format: `storage_available_kb=<number>`. 
Your Go program must parse this integer, convert it to Megabytes (where 1 MB = 1024 KB, using integer division), and write the result to a new file `/home/user/storage_metric.json`. 
The JSON file must have exactly this structure: `{"storage_mb": <calculated_value>}`.
After writing your code, execute it (e.g., using `go run /home/user/monitor.go`) so that `/home/user/storage_metric.json` is generated based on the current `device_storage.txt`. (If the text file does not exist in your environment, create a dummy one to test your code).

**2. Device Initialization Script**
Create a bash script at `/home/user/setup_iot.sh`. This script will be executed with root privileges later on the actual devices. It must contain the exact commands (one per line) to accomplish the following in order:
- Create a system group named `sensor-net`.
- Create a user named `metrics-agent` and set its primary group to `sensor-net`.
- Add a static network route directing traffic for the `172.16.0.0/12` subnet via the gateway `10.0.0.1` on the `eth0` interface using the `ip route` command.
- Establish an SSH tunnel that runs in the background (and does not execute a remote command) to forward the local port `8080` to `172.16.5.5:80` through an SSH jump host at `10.0.0.254` using the username `tunnel`. (Use standard OpenSSH client flags).

Ensure both `/home/user/monitor.go` and `/home/user/setup_iot.sh` are saved with your final solutions, and `/home/user/storage_metric.json` has been successfully generated.
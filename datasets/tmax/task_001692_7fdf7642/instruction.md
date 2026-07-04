You are an edge computing engineer deploying a mock sensor data logger to a fleet of IoT devices. Since you are operating in a restricted edge environment without root access, you need to simulate system configurations, specifically disk mounts and deployment pipelines, in the user space.

Your task is to create a deployment pipeline and a Python sensor logging script that dynamically reads a mock `fstab` configuration to find its target output directory.

Complete the following steps:

1. **Simulate the System Configuration (`fstab`)**
   Create a file named `/home/user/edge_fstab`. It must contain exactly the following line representing a mock mount configuration for the sensor drive:
   `UUID=EDGE_SENSOR_DRIVE /home/user/sensor_mnt ext4 defaults,noatime 0 2`

2. **Write the Python Sensor Application**
   Create a Python script at `/home/user/sensor_logger.py` that performs the following:
   - Parses the `/home/user/edge_fstab` file to find the target mount point for the device with `UUID=EDGE_SENSOR_DRIVE`.
   - Extracts the directory path (which should be `/home/user/sensor_mnt` based on the file).
   - Writes the exact string `EDGE_DATA_ACTIVE` to a file named `telemetry.log` inside that target directory.

3. **Create the Deployment Pipeline Script**
   Create a bash script at `/home/user/deploy.sh`. This script must:
   - Make the script executable (`chmod +x /home/user/deploy.sh` beforehand).
   - Read `/home/user/edge_fstab` using basic shell commands (e.g., `grep` and `awk`) to find the mount point for `UUID=EDGE_SENSOR_DRIVE`.
   - Create the target mount directory if it doesn't already exist.
   - Execute the Python script `/home/user/sensor_logger.py`.
   - Verify that the Python script successfully created the `telemetry.log` file and that it contains the string `EDGE_DATA_ACTIVE`.
   - If verification passes, the bash script must output exactly `DEPLOYMENT_SUCCESS` and redirect it to a log file at `/home/user/deploy_status.log`. If it fails, it should write `DEPLOYMENT_FAILED` to the same log file.

Execute your `/home/user/deploy.sh` script to complete the deployment and leave the system in the requested final state.
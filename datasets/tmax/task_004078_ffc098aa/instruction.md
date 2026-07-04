You are an edge computing engineer deploying to a fleet of remote IoT devices. Each device uses a legacy initialization script that requires interactive inputs and expects strict environment variable configurations for its timezone and locale to properly record sensor data.

Your task is to write a Python automation script at `/home/user/deploy_iot.py` that wraps this initialization script using the `pexpect` module. 

Here are the requirements for your Python script:
1. It must spawn the bash script located at `/home/user/iot_init.sh`.
2. It must pass the following environment variables specifically to the child process (do not change the system-wide settings):
   - `TZ` set to `Antarctica/Troll`
   - `LC_TIME` set to `fr_FR.UTF-8`
3. It must interact with the script by waiting for exact prompts and sending the correct responses:
   - When prompted with exactly `Configuration ready? [y/N]: `, send `y`.
   - When prompted with exactly `Device ID: `, send `EDGE-99X`.
4. Ensure the child process completes successfully.

After writing your script, execute it (`python3 /home/user/deploy_iot.py`). If successful, the `iot_init.sh` script will automatically generate a success log at `/home/user/iot_deploy.log`. 

Ensure that `pexpect` is used in your Python script to handle the interactive prompts.
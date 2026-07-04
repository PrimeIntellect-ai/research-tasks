You are a deployment engineer rolling out an update for our internal application, "DataVault". Because you do not have root access on this staging environment, system configurations are simulated using a mock directory structure in your home folder. 

Your task is to write and execute an idempotent deployment Bash script at `/home/user/deploy_update.sh` that performs the following configuration updates:

1. **Fstab Configuration Update:**
   Update the mock fstab file located at `/home/user/mock_etc/fstab`. You must add a new mount entry for the application's backup drive. 
   The exact line to append is:
   `UUID=99A1-B2C3 /home/user/app_backup ext4 defaults 0 2`
   *Requirement:* Your script must be idempotent. If the entry already exists, do not add it again. 

2. **Firewall Rules Update:**
   Update the mock firewall configuration file at `/home/user/mock_etc/firewall.rules`. You need to add a port forwarding rule to forward incoming traffic from port 8080 to the new application port 9090.
   The exact line to append is:
   `FORWARD TCP 8080 -> 9090`
   *Requirement:* This must also be idempotent. Do not add the rule if it already exists.

3. **Data Directory Permission Management:**
   Create a directory for the application data at `/home/user/app_data` if it doesn't exist.
   Set the permissions of this directory so that only the owner has read, write, and execute permissions (equivalent to `chmod 700`). No other user or group should have any access.

4. **Logging:**
   Your script must generate a log file at `/home/user/deploy.log` during execution. The log must contain exactly these three lines upon successful execution of the respective steps:
   `[SUCCESS] Mount configured`
   `[SUCCESS] Firewall updated`
   `[SUCCESS] Permissions set`

Execute your script once it is written. We will verify the final state of the mock configuration files, the directory permissions, and the deployment log. Ensure your script handles idempotency correctly (we will test this by running your script multiple times).
You are a cloud architect tasked with migrating a legacy service to a new deployment structure. You do not have root access on this environment, so you must prepare the migration artifacts, manage the local service lifecycle manually, and create a backup of the existing data. 

Complete the following migration phases:

**Phase 1: Backup Strategy**
There is a directory at `/home/user/legacy_data`. 
Create a compressed tar archive of this directory at `/home/user/backups/legacy_data.tar.gz`. 
Ensure the `backups` directory is created if it does not exist.

**Phase 2: Service Lifecycle Management**
You are provided with a web application at `/home/user/app.py`. Since we do not have system-wide systemd access, you must write a custom init script to manage this service.
Create a bash script at `/home/user/service_manager.sh` that accepts exactly one argument (`start`, `stop`, or `status`).
- `start`: Starts `python3 /home/user/app.py` in the background, saves its PID to `/home/user/app.pid`, and prints "Service started".
- `stop`: Reads the PID from `/home/user/app.pid`, kills the process, deletes the PID file, and prints "Service stopped".
- `status`: Checks if the PID file exists and the process is running. Prints "Service is running" or "Service is stopped".

Make the script executable and use it to `start` the service. Ensure the application is running and listening on port 8080.

**Phase 3: User Account & Firewall Migration (Python)**
Write a Python script at `/home/user/migration_builder.py` and execute it. The script must do the following:
1. Read `/home/user/legacy_users.csv` (Format: `username,role,email`).
2. Identify all users with the role `admin`.
3. Generate a bash script at `/home/user/create_admins.sh` containing the exact `useradd` commands needed to recreate these accounts on the target system. The commands must format as: `useradd -m -G admin <username>`.
4. Generate a mock firewall rules file at `/home/user/firewall.rules` containing exactly two `iptables` commands to forward port 80 to 8080 and accept port 8080:
   `iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
   `iptables -A INPUT -p tcp --dport 8080 -j ACCEPT`

Run your Python script so that `/home/user/create_admins.sh` and `/home/user/firewall.rules` are generated. Make `/home/user/create_admins.sh` executable.
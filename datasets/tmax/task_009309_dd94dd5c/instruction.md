You are a Cloud Architect preparing to migrate legacy services to a new Virtual Private Cloud (VPC). Since you do not currently have root access to the target staging server, you must generate the configuration scripts that the deployment automation will run, as well as build a custom C-based monitoring daemon that tracks the migration state.

Your objective is to create a monitoring program in C and a setup shell script that compiles it, launches it, and generates network, firewall, and storage configuration files.

Step 1: The Monitoring Daemon
Create a C program at `/home/user/monitor.c`. 
When compiled and run, this program must:
1. Run indefinitely in a loop.
2. Every 1 second, append the string `[SERVICE_MIGRATION_ACTIVE]\n` to `/home/user/migration.log`.
3. Intercept the `SIGTERM` signal. When it receives a `SIGTERM`, it must append exactly `[SERVICE_MIGRATION_STOPPED]\n` to `/home/user/migration.log` and then exit cleanly with status code 0.

Step 2: The Migration Preparation Script
Create an executable bash script at `/home/user/prepare_migration.sh`. When executed, this script must perform the following actions in order:
1. Compile `/home/user/monitor.c` to an executable named `/home/user/monitor`.
2. Start `/home/user/monitor` in the background.
3. Write the Process ID (PID) of the background monitor process to `/home/user/monitor.pid`.
4. Create a file `/home/user/firewall.sh` containing exactly the `iptables` command to forward incoming TCP traffic on interface `eth1` at port `443` to the internal destination IP `10.10.10.50` on port `8443`.
5. Create a file `/home/user/routes.sh` containing exactly the `ip route` command to route all traffic for the `10.10.10.0/24` subnet via the gateway `172.16.0.1` on interface `eth1`.
6. Create a file `/home/user/fstab.append` containing exactly the `fstab` entry to mount an NFS share from `10.10.10.50:/var/nfs` to `/mnt/shared` using the `nfs` filesystem, with options `rw,hard,intr` and `0 0` for dump and pass values.

Requirements:
- Do not run the generated configuration scripts (firewall, routes, fstab); only create them.
- Make sure `/home/user/prepare_migration.sh` has executable permissions.
- Ensure the generated files contain *only* the single line of configuration requested.
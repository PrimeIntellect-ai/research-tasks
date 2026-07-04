You are an observability engineer tuning the metric collection for a custom dashboard application. The standard monitoring agents are too heavy for a specific edge node, so you need to create a lightweight custom exporter in C and a shell script to manage its logs and backups.

Perform the following tasks:

1. Create a C program at `/home/user/exporter.c` and compile it to an executable named `/home/user/exporter`. 
The program must act as a health check by doing the following:
- Parse the network routing table located at `/proc/net/route` to find the default network interface. The default route is the row where the `Destination` column is exactly `00000000`. Extract the interface name (the `Iface` column, e.g., `eth0`).
- Check the size, in bytes, of the local datastore file located at `/home/user/app_data/db.sqlite`.
- Print exactly one line to standard output in the following JSON format:
`{"default_iface": "<interface_name>", "db_size": <size_in_bytes>}`

2. Create a bash script at `/home/user/collect_and_rotate.sh` that performs the following pipeline (combining log collection, rotation, and backup):
- Executes `/home/user/exporter` and appends its output to the log file `/home/user/metrics.log`.
- Copies the current `/home/user/metrics.log` to the backup directory `/home/user/backups/` with the filename `metrics_backup.log`.
- Empties (truncates) the `/home/user/metrics.log` file so it is exactly 0 bytes, preparing it for the next rotation cycle.

3. Make the bash script executable and run it exactly once.

Note: Assume the directories `/home/user/app_data/` and `/home/user/backups/`, as well as the file `/home/user/app_data/db.sqlite`, already exist. Do not use root privileges.
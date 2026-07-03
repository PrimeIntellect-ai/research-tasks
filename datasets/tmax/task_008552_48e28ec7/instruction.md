You are an infrastructure engineer automating bare-metal server provisioning. Your system extracts raw hardware inventory logs and maps them to actual network interfaces to configure static routing and environment variables.

You have been provided with a raw inventory dump at `/home/user/inventory_dump.log`. This file contains various host details, including lines that map MAC addresses to specific server roles.

Additionally, a mock `sysfs` filesystem has been generated for you at `/home/user/sys_mock/`. Inside this directory, there are subdirectories named after the system's network interfaces (e.g., `eno1`, `enp3s0`). Each of these subdirectories contains a file named `address` which holds the MAC address of that interface.

Your task:
1. Parse `/home/user/inventory_dump.log` to find the MAC address associated with the `storage_backend` role.
2. Search the mock filesystem at `/home/user/sys_mock/` to identify the network interface name (the subdirectory name) that corresponds to this MAC address. *Note: MAC addresses in the filesystem might be in lowercase, while the log might use uppercase.*
3. Write a script in Python, Perl, or Ruby at `/home/user/build_routes.py` (or `.rb` / `.pl`). This script must dynamically generate a bash script named `/home/user/apply_routes.sh`.
4. Run your script so that `/home/user/apply_routes.sh` is created.

The generated `/home/user/apply_routes.sh` must contain exactly two commands (plus the standard `#!/bin/bash` shebang):
1. An `ip route add` command to route the subnet `10.50.0.0/16` via gateway `10.50.0.1` out of the discovered `storage_backend` interface.
2. A command that appends the environment variable `STORAGE_IFACE=<interface_name>` to the file `/home/user/.bash_profile`.

Ensure the generated bash script has execute permissions. Do not actually execute the `apply_routes.sh` script, as you do not have root privileges to modify the actual system routing table. We will only verify the contents of `/home/user/apply_routes.sh`.
You are a backup operator tasked with testing the restoration of our critical network infrastructure configurations. The backup archive contains routing tables and firewall rules that need to be parsed and validated using our legacy C libraries. 

To complete this scenario, you must perform the following steps:

1. **Mount the Backup:**
   We have a simulated backup directory at `/app/backup_data`. Bind-mount this directory to `/home/user/restore_mnt` (you do not have root, so use a user-space bind mount or standard copy if bind-mounting fails, but ensure the path `/home/user/restore_mnt` contains the data). Add an entry for this to a local fake fstab file located at `/home/user/local_fstab` using the format: `/app/backup_data /home/user/restore_mnt none bind 0 0`.

2. **Fix the Legacy Library:**
   There is a vendored third-party library source provided at `/app/libnetconf`. This library is required to parse the old firewall rules, but its source code has a compilation issue due to a recent system migration. 
   - Identify and fix the missing header inclusion in `/app/libnetconf/net_parse.c`.
   - Fix the `Makefile` in `/app/libnetconf/` so that running `make` successfully produces the static library `libnetconf.a`.

3. **Timezone and Manifest Processing:**
   The backup includes a manifest file at `/home/user/restore_mnt/manifest.txt`. The timestamps in this file are sensitive to localization. 
   - Set your environment's locale to `C.UTF-8` and your Timezone (`TZ`) to `America/New_York`.
   - Use text processing tools (`awk`, `grep`) to extract all lines from `manifest.txt` where the third column is exactly "RESTORED". Save this to `/home/user/processed_manifest.txt`.

4. **Write the C Validation Utility:**
   Using C, write a program located at `/home/user/validate_ip_format.c` and compile it to `/home/user/validate_ip_format`. 
   This utility must read a single line of text from standard input (up to 128 characters) representing a restored network rule. It must output exactly `VALID\n` if the string starts with `ROUTE:` followed by exactly four digits, a dot, and an uppercase letter (e.g., `ROUTE:1234.A`), and `INVALID\n` otherwise. It must exit with status 0.

5. **SSH Tunneling Setup:**
   We have a local validation endpoint running on port 8080 (simulated). Set up an SSH tunnel using the local user `user` at `127.0.0.1` that forwards your local port 9090 to the remote validation endpoint at `127.0.0.1:8080`. Write the exact SSH command you used to `/home/user/ssh_tunnel_cmd.txt`.

Ensure all code compiles without warnings and all files are placed in their exact specified paths.
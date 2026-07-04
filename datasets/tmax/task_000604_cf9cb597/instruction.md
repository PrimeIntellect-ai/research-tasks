You are tasked with writing a Bash script that acts as a mock "GitOps Operator" for a simulated Kubernetes environment. The script must handle backups, parse simulated manifests to generate mount configurations, and create firewall rules without requiring root access.

Your script must be saved as `/home/user/operator.sh` and must be executable. When run, it should perform the following actions sequentially:

1. **Backup State:** 
   Archive the current contents of the `/home/user/active_manifests/` directory into a tarball located at `/home/user/backups/manifest_backup.tar.gz`. Use standard tar compression (`-czf`).

2. **Sync Manifests:**
   Copy all files from `/home/user/incoming_manifests/` to `/home/user/active_manifests/`, overwriting existing files if they have the same name.

3. **Generate Mount Rules (fstab):**
   Scan all `.yaml` files in the newly updated `/home/user/active_manifests/` directory. For every file that contains `kind: PersistentVolume`, extract the volume name and the host path. 
   Assume the YAML formatting is strict and predictable. The name will be on a line starting with exactly `  name: <vol_name>` and the path on a line starting with exactly `    path: <host_path>`.
   For each PersistentVolume found, append a line to `/home/user/mock_fstab` in the following format:
   `<host_path> /mnt/data/<vol_name> none bind 0 0`

4. **Generate Firewall Rules:**
   Scan all `.yaml` files in `/home/user/active_manifests/`. For every file that contains `kind: Service`, extract the `nodePort` value. 
   The port will be on a line starting with exactly `    nodePort: <port_number>`.
   For each Service found, append an iptables command to `/home/user/fw_rules.sh` to allow TCP traffic on that port:
   `iptables -A INPUT -p tcp --dport <port_number> -j ACCEPT`

Run your script once you have written it to ensure all output files (`manifest_backup.tar.gz`, `mock_fstab`, and `fw_rules.sh`) are generated correctly.

Constraints:
- Do not use Python, Perl, or other scripting languages; use pure Bash and standard coreutils (grep, awk, sed, tar, cp).
- Make sure to create the `/home/user/backups/` directory if it does not exist.
- Overwrite `/home/user/mock_fstab` and `/home/user/fw_rules.sh` (or create them empty) at the start of the script's execution so repeated runs do not duplicate entries.
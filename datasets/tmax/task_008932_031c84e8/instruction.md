You are tasked with preparing a deployment configuration package for a new isolated data-processing environment. Since you do not currently have root privileges on the target server, you must generate the directory structure and configuration scripts in a staging area. An automated system will later execute these scripts as root.

Your task has four phases. All work must be done inside the directory `/home/user/deploy_pkg`. Create this directory before beginning.

**Phase 1: Directory Structure and Links**
Create the base application directory structure inside the staging area:
1. Create the following directories:
   - `/home/user/deploy_pkg/app/bin`
   - `/home/user/deploy_pkg/app/logs`
   - `/home/user/deploy_pkg/app/data`
   - `/home/user/deploy_pkg/app/conf`
2. Create a symbolic link at `/home/user/deploy_pkg/app/current` that points to the `bin` directory (it must be a relative symlink pointing to `bin`, not an absolute path).

**Phase 2: Identity Management Script**
Write a bash script at `/home/user/deploy_pkg/create_identities.sh` that contains the exact commands to set up the required users and groups on the target system. The script must contain commands to:
1. Create a group named `dataproc` with a specific GID of `2000`.
2. Create a user named `data_ingest` with UID `2001` and primary group `dataproc` (using the group name or GID).
3. Create a user named `data_export` with UID `2002` and primary group `dataproc`.
(Do not execute this script, just create it).

**Phase 3: Fstab Configuration**
Create a file named `/home/user/deploy_pkg/fstab.append` containing exactly two lines formatted for `/etc/fstab` (assuming the application will reside at `/app` on the target root filesystem):
1. A bind mount that mounts `/var/log/dataproc` to `/app/logs`.
2. An NFSv4 mount that mounts `10.0.0.5:/export/data` to `/app/data` with read-only (`ro`) permissions.
Use standard fstab columns (fs_spec, fs_file, fs_vfstype, fs_mntops, fs_freq, fs_passno). Set the last two columns (freq and passno) to `0 0` for both entries.

**Phase 4: Firewall Configuration Script**
Write a bash script at `/home/user/deploy_pkg/firewall.sh` containing `iptables` commands to configure the host firewall. The script must:
1. Append a rule to the `INPUT` chain to allow incoming TCP traffic on port `8080`.
2. Append a rule to the `PREROUTING` chain in the `nat` table to `REDIRECT` incoming TCP traffic on port `80` to port `8080`.
3. Append a rule to the `INPUT` chain to `DROP` all traffic originating from the IP address `192.168.1.100`.

Ensure all requested files are created exactly at the specified paths.
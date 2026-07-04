As a network engineer troubleshooting connectivity for a custom user-space routing daemon, you need to write a diagnostic tool to extract the correct configuration state from the system's mock configuration files. 

The daemon's configuration directory is stored on a dynamically mounted filesystem, and incoming HTTP traffic is port-forwarded via iptables rules to the daemon's actual listening port.

Write a C program at `/home/user/analyzer.c` that performs the following steps:
1. Parse the mock file `/home/user/fstab.mock` to find the mount point path for the filesystem associated with `UUID=NET-CONFIG-FS`.
2. Locate the `config.ini` file inside that discovered mount point directory. 
3. Implement a backup strategy by having your C program copy this `config.ini` file to `/home/user/config.ini.bak`.
4. Parse the local firewall rules dump located at `/home/user/iptables.dump` to find the port forwarding rule. Specifically, find the local port that incoming TCP traffic on `--dport 80` is redirected to via `--to-ports`.
5. Write the extracted information to a final log file at `/home/user/resolution.log` with exactly the following format:
   ```
   MountPoint: <extracted_mount_point>
   ForwardedPort: <extracted_port>
   ```

After writing the C program, compile it using `gcc /home/user/analyzer.c -o /home/user/analyzer` and execute it to generate the backup and the `resolution.log` file.

Do not hardcode the paths or ports found in the mock files into your C program; it must parse them dynamically.
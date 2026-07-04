As a site administrator managing user accounts, you need to automate the preparation of network and storage configuration files for user isolation environments. Since you do not currently have root access on this jump server, you must write a robust Bash script that generates the necessary `fstab` entries and `iptables` port forwarding commands that will be applied by the system provisioning tool later.

Write a Bash script at `/home/user/generate_configs.sh` and execute it. 

Your script must read a CSV file located at `/home/user/requests.txt`. Each line in this file contains a request for a user environment in the format:
`username,external_port,jail_share_path`

Your script must perform the following tasks:
1. Parse the CSV file robustly. If a line does not have exactly 3 comma-separated fields, it must be considered malformed.
2. For malformed lines, append the exact raw line to `/home/user/error.log` and skip to the next line.
3. For valid lines, generate an `fstab` entry that bind-mounts `/data/common_share` to the requested `jail_share_path` in read-only mode. Append this entry to `/home/user/fstab_generated`. The format should be:
   `<source> <destination> none bind,ro 0 0`
4. For valid lines, generate an `iptables` command that forwards incoming TCP traffic on the user's `external_port` to an internal jump server at `10.0.0.5:22`. Append this command to `/home/user/port_forwards.rules`. The command format must exactly match:
   `iptables -t nat -A PREROUTING -p tcp --dport <external_port> -j DNAT --to-destination 10.0.0.5:22`

Ensure your script processes all lines, clears the output files (`/home/user/error.log`, `/home/user/fstab_generated`, `/home/user/port_forwards.rules`) if they already exist before processing, and gracefully handles empty lines by ignoring them. Run your script so the output files are generated.
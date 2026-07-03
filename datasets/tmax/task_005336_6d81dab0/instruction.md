You are acting as an infrastructure engineer automating the provisioning validation for a fleet of simulated servers. You need to write a Python validation script that audits system configurations related to network routing, disk usage, timezones, and SSH access.

Your task is to create a Python script at `/home/user/system_audit.py`. When run, this script must analyze several mock system files and output a final report to `/home/user/audit_report.json`.

The script must perform the following four audits:

1. **Storage Monitoring (Disk Quota Check):**
   Calculate the total disk space (in bytes) used by the directory `/home/user/app_data/` and all of its subdirectories and files. Do not follow symlinks. 
   *JSON Key:* `app_data_size_bytes` (integer)

2. **Network Routing Configuration:**
   Parse the mock routing table provided at `/home/user/mock_routes.txt`. This file contains the output of an `ip route` command. Your script must extract the IPv4 address of the default gateway (the IP following `default via`).
   *JSON Key:* `default_gateway` (string)

3. **Timezone Configuration Check:**
   Read the desired timezone from a JSON configuration file located at `/home/user/config.json` (under the key `"timezone"`). Compare this value to the actual system timezone found as plain text inside `/home/user/mock_etc_timezone`. Return `true` if they match exactly (case-sensitive, ignoring leading/trailing whitespace), and `false` otherwise.
   *JSON Key:* `timezone_match` (boolean)

4. **SSH Configuration Audit (Silently Rejected Logins):**
   Parse the mock SSH configuration file located at `/home/user/mock_ssh_config`. Some `Host` blocks have been configured to silently reject key-based logins by setting `PubkeyAuthentication no`. Find all `Host` declarations where `PubkeyAuthentication no` is explicitly defined anywhere within that host's block (before the next `Host` declaration or the end of the file). Note that SSH directives are case-insensitive and spacing may vary.
   *JSON Key:* `rejected_ssh_hosts` (list of strings, representing the names of the hosts)

**Output Format:**
The script must output a strictly valid JSON file at `/home/user/audit_report.json` with the following structure:
```json
{
  "app_data_size_bytes": 10240,
  "default_gateway": "192.168.1.1",
  "timezone_match": true,
  "rejected_ssh_hosts": ["web-prod-01", "db-backup"]
}
```

Make sure `/home/user/system_audit.py` is executable and successfully generates the report when run with `python3 /home/user/system_audit.py`. Do not hardcode the expected answers; your script must programmatically parse the target files.
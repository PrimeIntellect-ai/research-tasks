You are tasked with analyzing a large, multi-line audit log from a configuration manager and extracting specific access control changes to generate a firewall application script.

You have been provided with a large log file at `/home/user/config_audit.log`. 
This file contains hundreds of thousands of multi-line records tracking configuration changes across various system services.

The log file has the following multi-line format for each record:
```
[RECORD_START]
Timestamp: <unix_timestamp>
Service: <service_name>
Action: <action>
TargetIP: <ip_address>
Details:
<arbitrary multi-line text, logs, or diffs>
<...>
Status: <SUCCESS or FAILURE>
[RECORD_END]
```

Your objective is to:
1. Write a highly efficient Python script (e.g., using streaming I/O or `mmap`) to parse this file. You must handle the multi-line nature of the records.
2. Extract the `TargetIP` for all records that strictly meet ALL of the following criteria:
   - `Service: firewall`
   - `Action: ALLOW`
   - `Status: SUCCESS`
3. Transform these extracted IP addresses into a bash script located at `/home/user/apply_firewall.sh`.
4. The bash script must:
   - Start with `#!/bin/bash`
   - Contain exactly one `iptables` command per unique extracted IP address, sorted in ascending lexicographical order by the IP string.
   - The command format must be exactly: `iptables -A INPUT -s <IP_ADDRESS> -j ACCEPT`
5. Make the script executable (`chmod +x /home/user/apply_firewall.sh`).

Example of `/home/user/apply_firewall.sh` output:
```bash
#!/bin/bash
iptables -A INPUT -s 10.0.0.5 -j ACCEPT
iptables -A INPUT -s 192.168.1.100 -j ACCEPT
```

Ensure your Python script is robust against variations in the "Details" section, which may contain arbitrary text, including words like "Status" or "Service" (though the true fields are always at the root of the record as shown in the template).
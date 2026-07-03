You are a cloud architect tasked with migrating several legacy virtualized services to a newly structured environment. You have been provided with an architectural diagram of the new deployment topology, located at `/app/topology.png`. This image details the strict mapping between Service Names, their assigned VNC ports for VM management, and their allowed host storage directory constraints.

During the migration, an automated tool generated thousands of VM configuration files. Unfortunately, the generator was flawed. Many configurations contain critical misconfigurations: they assign incorrect VNC ports, attempt directory traversals (e.g., using `../`), or point to symlinks that resolve to unauthorized paths outside their designated storage constraints.

You must build an executable validation script at `/home/user/validate_vm` (you may use Python, Bash, or any other installed language, but it must be executable directly). 

Your script must take a single argument: the absolute path to a VM configuration JSON file. 
Example JSON structure:
`{"service": "auth", "vnc_port": 5901, "host_mount": "/home/user/vms/auth_data/sessions"}`

**Validation Rules:**
1. Extract the authoritative Service Name, VNC Port, and Base Storage Path mappings from `/app/topology.png`.
2. Ensure the `vnc_port` in the JSON exactly matches the port specified for that service in the topology diagram.
3. Ensure the `host_mount` path is completely enclosed within the service's Base Storage Path. 
4. **Crucial Security Check:** The `host_mount` path might contain symlinks or relative traversals (`../`). Your script must resolve the absolute real path of the `host_mount` and verify that the final canonical path strictly starts with the canonical Base Storage Path for that service. If it resolves outside the base path, it must be rejected.

**Expected Output:**
- If the configuration strictly adheres to the rules, your script must exit with status code `0`.
- If the configuration violates *any* rule (wrong port, path escape, invalid service), your script must exit with a non-zero status code (e.g., `1`).

To help you develop and refine your script, two directories have been provided:
- `/app/configs/clean/` - Contains known good configurations.
- `/app/configs/evil/` - Contains known bad configurations (wrong ports, symlink escapes, etc.).

An automated verifier will test your `/home/user/validate_vm` script against a hidden set of clean and evil configurations. Your script must correctly classify 100% of the files.
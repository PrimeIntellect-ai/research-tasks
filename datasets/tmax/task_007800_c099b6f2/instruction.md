You are an infrastructure engineer setting up a lightweight GitOps provisioning pipeline for edge routers. Since you do not have root access on the build server, your goal is to set up a Git repository and a hook that automatically generates system configuration files (for networking and firewalls) whenever a new configuration payload is pushed.

Please perform the following steps:

1. Create a directory `/home/user/provision_out`.
2. Initialize a bare Git repository at `/home/user/edge-config.git`.
3. Create a `post-receive` Git hook in `/home/user/edge-config.git/hooks/post-receive`. The hook MUST be written in Python 3 (use `#!/usr/bin/env python3`). Make sure the hook is executable.

The `post-receive` hook must do the following:
- Read lines from standard input (which Git provides as `oldrev newrev refname`).
- Using the `newrev` commit hash, extract the file named `router.json` from the root of the repository. (Hint: you can use `git cat-file` or `git show` via the `subprocess` module).
- Parse `router.json`. The JSON will have the following schema:
  ```json
  {
    "interfaces": {
      "<iface_name>": {
        "ip": "<cidr_address>",
        "gateway": "<ip_address>" // gateway is optional
      }
    },
    "port_forwarding": [
      {
        "in_port": <int>,
        "out_ip": "<ip_address>",
        "out_port": <int>
      }
    ]
  }
  ```
- Generate a Netplan configuration file at `/home/user/provision_out/netplan.yaml` with exactly this structure based on the JSON:
  ```yaml
  network:
    version: 2
    ethernets:
      <iface_name>:
        addresses:
          - <cidr_address>
        routes:             # Only include 'routes' if a gateway is specified in the JSON
          - to: default
            via: <gateway_ip>
  ```
  *(Note: Maintain proper YAML indentation (2 spaces per level).)*

- Generate an nftables configuration file at `/home/user/provision_out/nftables.conf` for the port forwarding rules. For each rule in the `port_forwarding` list, generate a single line using this exact template format:
  ```
  add rule ip nat PREROUTING tcp dport <in_port> counter dnat to <out_ip>:<out_port>
  ```
  The file should contain nothing else except these port forwarding lines (one per rule, in the same order as the JSON array).

Ensure your setup is complete and fully functional. A test suite will push a commit containing a `router.json` to your bare repository and verify that the output files in `/home/user/provision_out/` are generated correctly.
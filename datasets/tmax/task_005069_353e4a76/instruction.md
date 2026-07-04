You are a system administrator tasked with managing secure access to internal services across different remote environments. To streamline this process without requiring root access, you will create a custom configuration system that acts like `fstab`, but for SSH port forwarding. You will also write an interactive Python script to parse this file and generate the appropriate tunneling commands.

Your task has three parts:

**Part 1: SSH Configuration**
Create the SSH configuration file at `/home/user/.ssh/config` to define two jump hosts. Ensure the file has the correct permissions.
1. Alias: `jump_web`
   - Hostname: `ssh.web-infra.example.com`
   - User: `webops`
   - Port: `2222`
2. Alias: `jump_db`
   - Hostname: `ssh.data-infra.example.internal`
   - User: `dbadmin`
   - Port: `22`

**Part 2: The "Port fstab" Configuration**
Create a configuration file at `/home/user/port_fstab` that lists the tunnels. Use the following space-separated format (similar to an fstab file):
`<local_port> <remote_target>:<remote_port> <ssh_alias> <extra_ssh_options>`

Add the following two entries to the file (and add a comment line starting with `#` at the top):
- Forward local port `8080` to `10.1.1.50:80` via `jump_web` with options `-N -T`
- Forward local port `5432` to `192.168.100.10:5432` via `jump_db` with options `-N -f`

**Part 3: Interactive Python Script**
Create a Python script at `/home/user/tunnel_builder.py` that does the following:
1. Opens and reads `/home/user/port_fstab`. It must skip any empty lines or lines starting with `#`.
2. For each valid entry, extract the fields.
3. Interactively prompt the user using `input()` with the exact text:
   `Enable tunnel to <remote_target>:<remote_port> on local port <local_port>? (y/n): `
   *(Note: Replace the bracketed placeholders with the actual parsed values).*
4. If the user inputs `y`, append the corresponding SSH port forwarding command to a bash script located at `/home/user/start_tunnels.sh`.
5. The generated commands in `/home/user/start_tunnels.sh` must be formatted exactly as:
   `ssh -L <local_port>:<remote_target>:<remote_port> <extra_ssh_options> <ssh_alias>`
6. Ensure `/home/user/start_tunnels.sh` starts with `#!/bin/bash` and is made executable by your Python script (using `os.chmod`). It should overwrite the file if it already exists.

Complete these steps to finish the task. Do not execute the generated `start_tunnels.sh` script, just ensure it is correctly generated when `tunnel_builder.py` is run interactively.
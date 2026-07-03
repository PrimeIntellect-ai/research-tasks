You are a monitoring specialist setting up an automated active-defense alert system. We have an issue where our SSH configuration silently rejects invalid key-based logins, leaving a specific log signature in our system logs. 

We need to extract the offending IP and use our interactive deployment tool to push a staged firewall block.

Your tasks are to:
1. Parse the log file located at `/home/user/auth.log`. Look for lines matching the exact format:
   `[sshd] Connection closed by authenticating user <username> <IP_ADDRESS> port <port> [preauth]`
   Find the **single** IP address that has *exactly* 4 occurrences of this message.

2. Write an `expect` script located at `/home/user/auto_deploy.exp`. This script must automate our interactive firewall deployment tool located at `/home/user/deploy_fw`.
   
   The `/home/user/deploy_fw` tool is interactive and prompts exactly as follows (wait for these exact strings):
   - Prompt 1: `Target IP to block: ` (Provide the IP you extracted from the log)
   - Prompt 2: `Select deployment stage (rolling/staged/all): ` (Provide the string `staged`)
   - Prompt 3: `Confirm deployment (y/n): ` (Provide `y`)

3. Execute your `expect` script. If successful, the `/home/user/deploy_fw` tool will generate a log at `/home/user/deployment_success.log`. 

Requirements:
- Ensure your `expect` script uses the correct shebang (`#!/usr/bin/expect`).
- Do not modify `/home/user/auth.log` or `/home/user/deploy_fw`.
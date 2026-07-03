You are a system administrator tasked with automating configuration and connectivity diagnostics for a legacy "Secure Gateway" appliance. Because this appliance lacks an API, all administration must be done via an interactive CLI console.

Your environment contains the following:
1. A mock interactive appliance tool located at `/home/user/sg-console.sh`.
2. A list of required network routes in `/home/user/routes.txt`. Each line contains a destination subnet and a gateway IP, separated by a space (e.g., `10.0.1.0/24 192.168.1.254`).

Your task involves writing an `expect` script to interact with the appliance, a Bash wrapper to automate reading the routes, and configuring your environment.

Step 1: Environment Variables
The appliance requires credentials. Configure your `/home/user/.bashrc` to export two environment variables:
- `SG_USER` set to `admin`
- `SG_PASS` set to `secret123`
*(Note: Ensure you export these exactly as written so scripts running in new interactive shells inherit them).*

Step 2: The Expect Script
Create an expect script at `/home/user/auto-sg.exp`. This script must:
1. Accept two arguments: the destination subnet (arg 0) and the gateway IP (arg 1).
2. Spawn the interactive console: `/home/user/sg-console.sh`
3. Wait for the `Username:` prompt and send the value of the `SG_USER` environment variable.
4. Wait for the `Password:` prompt and send the value of the `SG_PASS` environment variable.
5. Wait for the `SG>` prompt.
6. Send the command to add the route: `route add <destination> <gateway>`
7. Wait for the `SG>` prompt again.
8. Send the command to verify connectivity: `ping <destination>`
9. Wait for the `SG>` prompt again, then send `exit`.
Make sure the script captures the output of the console natively to standard output.

Step 3: The Bash Automation Script
Create a bash script at `/home/user/diagnose.sh`. This script must:
1. Read `/home/user/routes.txt` line by line.
2. For each line, invoke your `auto-sg.exp` script passing the destination and gateway as arguments.
3. Parse the output of the `auto-sg.exp` script. If the output contains the string "Reply from" followed by the destination, it means the ping succeeded.
4. For every successful ping, append a line exactly matching this format to `/home/user/success.log`:
   `[SUCCESS] <destination> via <gateway>`

Ensure both `/home/user/auto-sg.exp` and `/home/user/diagnose.sh` are executable (`chmod +x`). 
You can install `expect` if it is not already installed on the system using the system package manager.
Execute your `diagnose.sh` script to generate `/home/user/success.log` as the final artifact.
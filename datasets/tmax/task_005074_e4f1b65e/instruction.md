You are an infrastructure engineer setting up a lightweight, automated provisioning listener on a jumpbox. You have been provided with a source package for a simple bash-based webhook server, but it contains a few issues out-of-the-box. 

Your objective is to fix the package, install it, write the provisioning pipeline script, and configure the webhook server to run as a daemon.

Here are the requirements:

1. **Fix and Install the Vendored Webhook Server:**
   - The source code is located at `/app/bash-webhook-1.0`.
   - The `Makefile` currently attempts to install the binary to `/usr/local/bin/`. Since you do not have root access, modify the Makefile or your environment so that running `make install` places the binary `webhook-server` into `/home/user/.local/bin/`.
   - The `webhook-server` script has a bug: when handling incoming requests, it incorrectly checks the HTTP method by reading a variable called `$REQUEST_METHOD` instead of the internally parsed `$HTTP_METHOD` variable. Find this bug in the source, fix it, and install the package.

2. **Create the Provisioning Script:**
   - Create a script at `/home/user/provision.sh`.
   - The script must accept a single argument: the project name (a string).
   - The script must append the line: `[$(date -I)] Provisioning project: <project_name>` to the log file `/home/user/logs/deploy.log`.
   - Ensure the script is executable.

3. **Configure Permissions and Logs:**
   - Create the directory `/home/user/logs/`.
   - Set the permissions on `/home/user/logs/` strictly to `750`.
   - Create an empty `/home/user/logs/deploy.log` file with permissions set strictly to `640`.

4. **Run the Webhook Server:**
   - The `webhook-server` binary accepts three arguments: the port, the endpoint path, and the command to execute.
   - Start the server in the background so it listens on port `8080`.
   - It should listen on the endpoint `/deploy`.
   - When the endpoint receives an HTTP POST request, it expects a JSON body like `{"project": "example-app"}`. The webhook server automatically extracts the value of the "project" key and passes it as the first argument to the configured command.
   - Configure the server to execute `/home/user/provision.sh` when the webhook is triggered.

Leave the server running in the background. Do not stop it. An automated test will send a real HTTP POST request to your server and verify both the HTTP response and the side-effect in your log file.
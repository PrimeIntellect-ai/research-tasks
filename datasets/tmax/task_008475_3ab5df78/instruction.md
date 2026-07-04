You are an infrastructure engineer automating the provisioning of a local web service without root access. 

You have been provided an interactive configuration script located at `/home/user/init_server.sh`. This script asks three questions interactively:
1. "Enter Server Name: "
2. "Enter Port: "
3. "Enter Directory: "

Your task has two parts:

**Part 1: Interactive Automation (Expect)**
Write an Expect script named `/home/user/automate_init.exp` that executes `/home/user/init_server.sh` and automatically provides the following answers:
- Server Name: `AutoProvisionedWeb`
- Port: `8080`
- Directory: `/home/user/webroot`

Run your Expect script so that it generates the configuration file (`/home/user/server.conf`) and the target directory.

**Part 2: Process Supervision (Bash)**
Write a Bash script named `/home/user/watchdog.sh` that acts as a user-space process supervisor. The script must:
1. Source the generated `/home/user/server.conf` file to get the `$PORT` and `$DIR` variables.
2. Start a Python HTTP server in the background using the command: `python3 -m http.server $PORT --directory $DIR`
3. Enter an infinite loop that checks the status of this specific python server process every 1 second.
4. If the python HTTP server process crashes or is killed, the watchdog must:
   - Restart the python server.
   - Append the exact string `[RESTART] python http server crashed, restarting...` to a log file at `/home/user/watchdog.log`.

Finally, execute `/home/user/watchdog.sh` in the background and ensure it is running and actively supervising the web server. Do not exit the terminal or stop the background process.
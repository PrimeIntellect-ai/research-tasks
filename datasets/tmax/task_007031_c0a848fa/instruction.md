You are a Site Reliability Engineer (SRE). We have a legacy python-based monitoring console located at `/home/user/legacy_monitor.py`. Due to a misconfiguration (similar to an SSH config silently rejecting key-based logins), its automated API is broken, and it currently only accepts interactive terminal logins. 

Your task is to use `expect` to automate the interaction with this legacy console to fetch the system uptime.

Specifically, write and execute a script that accomplishes the following:
1. Spawns the interactive program using `python3 /home/user/legacy_monitor.py`.
2. Handles the login:
   - Responds to the `Username: ` prompt with `admin`.
   - Responds to the `Password: ` prompt with `sre_pass_2024`.
3. Interacts with the command interface (which uses the prompt `monitor> `):
   - The system requires the locale/timezone to be explicitly set to UTC before it can accurately report uptime. Send the command `set_tz UTC`.
   - Wait for the next prompt and send the command `get_uptime`.
   - The program will output something like `UPTIME_VALUE: <value>`.
   - Send the `exit` command to close the session gracefully.
4. Parse the output of your automation to extract *only* the actual uptime value (e.g., if the output is `UPTIME_VALUE: 99.99%`, you extract `99.99%`).
5. Save this exact extracted string into `/home/user/uptime.log` with no trailing spaces (a trailing newline is fine).

You must complete this task by writing the necessary automation code, executing it, and ensuring `/home/user/uptime.log` is successfully created with the correct parsed content.
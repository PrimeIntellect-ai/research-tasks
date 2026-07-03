You are a deployment engineer rolling out an update for our custom QEMU VM management service. The core service is a lightweight C program that generates virtualization startup commands, but the previous engineer left it broken and incomplete.

Currently, the source code is located at `/home/user/src/vm_service.c`. 
It has a critical bug: it crashes (segfaults) if the `VNC_DISPLAY` environment variable is not set. 

Your tasks are to:
1. **Fix the C program**: Edit `/home/user/src/vm_service.c` so that if the `VNC_DISPLAY` environment variable is missing or empty, it defaults to the string `:1`. The program should print `Starting QEMU on VNC display <display_value>\n` to standard output and exit gracefully (return 0).
2. **Compile the program**: Compile the fixed C code into an executable located exactly at `/home/user/bin/vm_service`. (Create the `/home/user/bin` directory if it doesn't exist).
3. **Automate the Deployment & Log Rotation**: Create an executable bash script at `/home/user/deploy.sh` that performs the following steps in order:
    a. Appends the line `export VNC_DISPLAY=:5` to the user's `/home/user/.bashrc` file.
    b. Exports `VNC_DISPLAY=:5` in the current script environment.
    c. Executes `/home/user/bin/vm_service` and appends its standard output to `/home/user/logs/service.log`. (Create `/home/user/logs` if it doesn't exist).
    d. Simulates a log rotation by copying `/home/user/logs/service.log` to `/home/user/logs/service.log.bak`, and then completely emptying (truncating to 0 bytes) the original `/home/user/logs/service.log` file.

Do not execute the `deploy.sh` script yourself. Provide the necessary terminal commands to fix the C code, compile it, and write the deployment script. The automated verification system will run `/home/user/deploy.sh` and inspect the resulting files and system state.
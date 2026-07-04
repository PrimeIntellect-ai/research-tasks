You are a container specialist managing a microservices stack. Your reverse proxy is returning a "502 Bad Gateway" error because it cannot find the upstream UNIX socket of a backend C daemon. The backend daemon writes its socket to a hardcoded temporary directory, but the proxy expects it in a specific runtime mapping directory.

Your task is to fix the environment, compile the backend daemon, and write an automation script that bridges this gap and brings the stack online safely.

Here is the current state of the system and your requirements:

1. **Environment & Directory Setup**:
   - Create the directories `/home/user/bin`, `/home/user/proxy/run`, and `/home/user/_service/tmp`.
   - Update `/home/user/.bash_profile` to export the environment variable `SOCKET_MAPPING_DIR="/home/user/proxy/run"`. Also, append `/home/user/bin` to the `PATH`. 

2. **Backend C Daemon**:
   - There is a C source file located at `/home/user/_service/daemon.c` (this will be present on the system).
   - Compile this C file into an executable named `daemon` and place it in `/home/user/bin/`.

3. **Automation Script**:
   - Write a shell script at `/home/user/bin/start_stack.sh` and make it executable.
   - The script must perform the following actions in order:
     a. **Storage Check**: Use `df -k /home/user` and `awk` to check the available space on the filesystem hosting the home directory. If the available space is less than 50000 KB, the script should exit with status code 1.
     b. **Path Extraction**: Read `/home/user/_service/daemon.c` using text processing tools (`grep`, `awk`, or `sed`) to dynamically extract the socket path defined in the macro `#define SOCKET_PATH "..."`. Do not hardcode the path in your script.
     c. **Daemon Startup**: Execute the compiled `daemon` binary in the background.
     d. **Link Management**: Wait for 1 second (`sleep 1`) to allow the daemon to create its socket. Then, create a symbolic link from the proxy's expected socket path (`$SOCKET_MAPPING_DIR/upstream.sock`) pointing to the extracted backend socket path.
     e. **Validation**: Execute the existing proxy check script located at `/home/user/proxy/check_upstream.sh`. Redirect its standard output to `/home/user/proxy/status.log`.

To complete the task, execute your `/home/user/bin/start_stack.sh` script so that the daemon is running, the symlink is created, and the `status.log` file is populated.
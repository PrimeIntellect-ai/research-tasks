I am managing a local microservices environment and troubleshooting a simulated "502 Bad Gateway" issue. Our upstream service (written in C) is failing to receive connections because it is binding to the wrong Unix domain socket path. 

The source code for the service is located at `/home/user/app/server.c`. It reads the socket path from the `UPSTREAM_SOCKET` environment variable, but there is a bug in the code causing the socket path to be incorrectly truncated when setting up the `sockaddr_un` struct.

Please perform the following tasks to fix the pipeline:

1. **Fix the C Code**: Modify `/home/user/app/server.c` so that it correctly copies the entire string from the `UPSTREAM_SOCKET` environment variable into the `sun_path` field (ensure it's safely bounded by `sizeof(addr.sun_path) - 1`). 
2. **Compile the Service**: Compile the fixed C code to the executable `/home/user/app/server` using `gcc`.
3. **Environment Configuration**: Edit `/home/user/.bashrc` and export the following variables so they are available in future interactive sessions:
   - `UPSTREAM_SOCKET=/home/user/run/microservice.sock`
   - `TZ=Etc/UTC` (to enforce a consistent timezone for our logs)
4. **CI Integration Script**: Write an executable bash script at `/home/user/ci_test.sh`. The script must:
   - Source `/home/user/.bashrc` to load the variables.
   - Start `/home/user/app/server` in the background.
   - Wait for 1 second to let the server bind to the socket.
   - Connect to the socket using `nc -U $UPSTREAM_SOCKET`. (The C server is programmed to accept a single connection, reply with "OK\n", and exit).
   - Redirect the output of the `nc` command to `/home/user/ci_result.log`.

Ensure `/home/user/run` exists before running your CI script. Run `/home/user/ci_test.sh` to confirm everything works and verify that `/home/user/ci_result.log` contains the expected output.
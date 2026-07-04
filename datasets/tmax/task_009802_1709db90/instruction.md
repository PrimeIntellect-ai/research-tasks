You are a Site Reliability Engineer (SRE) tasked with building a custom lightweight monitoring tool and its orchestration script to check the uptime of a local service during a staged deployment.

Your objective is to write a C++ program that acts as a TCP ping utility, and a robust Bash script that manages a dummy service, tests the C++ program against it, and records the state.

**Step 1: Write the C++ Monitoring Utility**
Create a C++ program at `/home/user/src/tcp_ping.cpp` (you will need to create the `src` directory).
The program must:
1. Accept exactly one command-line argument: a port number (integer).
2. Attempt to establish a TCP connection to `127.0.0.1` on the specified port.
3. If the connection is successful, print exactly the string `UP` to standard output (followed by a newline).
4. If the connection is refused or fails, print exactly the string `DOWN` to standard output (followed by a newline).
5. Exit cleanly with a return code of 0 in either case. (Only return non-zero if the wrong number of arguments is provided).

**Step 2: Write the Orchestration Script**
Create a robust bash script at `/home/user/run_checks.sh`. The script must perform the following actions in order:
1. Create the directory `/home/user/bin` if it does not exist.
2. Compile `/home/user/src/tcp_ping.cpp` using `g++` into an executable located at `/home/user/bin/tcp_ping`.
3. Start a dummy service in the background listening on TCP port `8888`. You can use `python3 -m http.server 8888` for this.
4. Capture the PID of the background service and wait for 2 seconds to ensure it has fully started.
5. Execute `/home/user/bin/tcp_ping 8888` and append its standard output to `/home/user/uptime.log`.
6. Terminate (kill) the background dummy service using its captured PID. Wait for 2 seconds to ensure it has fully shut down.
7. Execute `/home/user/bin/tcp_ping 8888` again, appending its standard output to `/home/user/uptime.log`.

Make sure your bash script is executable (`chmod +x`). 
Once both files are created, run your bash script `/home/user/run_checks.sh` to generate the final `/home/user/uptime.log`.
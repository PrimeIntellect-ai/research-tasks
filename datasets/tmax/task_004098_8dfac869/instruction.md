You are tasked with fixing a broken capacity planning collection system. The system consists of a network simulation daemon (`net_sim.py`) and a metrics collector written in C (`planner.c`). 

Currently, the collector fails to start due to missing configuration directories, compilation errors, and race conditions during startup (the collector tries to connect to the daemon before it finishes binding to its port).

Your objectives are:
1. **Directory Management**: The C program expects its configuration file to be located at `/home/user/config/settings.conf`. The actual configuration file has been deployed to `/home/user/capacity-config/settings.conf`. Create a symbolic link so the C program can find its configuration without modifying its hardcoded path.
2. **Fix and Compile the C Program**: Fix the compilation errors in `/home/user/planner.c` (missing standard networking headers and a missing return statement in `main`). Compile it to an executable named `/home/user/planner`.
3. **Robust Supervisor Script**: Write a bash script at `/home/user/start_services.sh` that acts as a process supervisor. The script must:
    - Use robust error handling (e.g., fail on unhandled errors).
    - Start the network simulation daemon in the background using: `python3 /home/user/net_sim.py &`
    - Actively poll and wait for `127.0.0.1` port `8888` to become available before starting the collector. (The python daemon takes about 2 seconds to start).
    - Execute the compiled `/home/user/planner` binary.
    - Redirect the standard output of the `planner` binary to `/home/user/planner_output.log`.

Make sure `/home/user/start_services.sh` is executable and run it so that the final `/home/user/planner_output.log` file is generated. The automated test will verify the contents of this log file, the existence of the symlink, and the successful compilation of the binary.
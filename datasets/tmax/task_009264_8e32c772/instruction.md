I have a custom C-based application that acts as a mock server, managed by a local git repository and a simple process supervisor. 

Currently, the service is failing to start. The source code is located at `/home/user/repo/server.c`. I have a local Git `post-commit` hook configured so that whenever a commit is made, it automatically compiles `server.c` and restarts my supervisor script (`/home/user/repo/supervisor.sh`). 

If you look at the supervisor logs or try to run the server, you will see it crashes immediately with an "Error opening PID file" message. This is because it attempts to write its PID to `/home/user/run/server.pid`, but the directory `/home/user/run` does not exist on the filesystem.

Your task is to:
1. Modify `/home/user/repo/server.c` so that the program dynamically creates the `/home/user/run` directory with `0755` permissions using the C `mkdir` function (from `<sys/stat.h>`) right before it tries to open the PID file.
2. Commit your changes to the Git repository located in `/home/user/repo` with the exact commit message: `Fix PID directory`.
3. The `post-commit` hook will automatically compile the code and start the supervisor. Wait a second to ensure it is running.
4. Verify the server is running, and write the PID of the running `server` process (which should now also be correctly written to `/home/user/run/server.pid`) into a file at `/home/user/solution.txt`.

Do not manually create the `/home/user/run` directory using shell commands; the directory must be created by your modified C program when it starts.
You are acting as a cloud architect migrating a legacy backend service. The internal API gateway is currently throwing the equivalent of a 502 Bad Gateway error because it cannot communicate with our C++ backend service. The backend is supposed to listen on a Unix domain socket, but the source code is currently hardcoded to an old legacy path that the new environment doesn't use.

Your task is to fix the code, compile it, and write a watchdog script to ensure the service stays up, simulating a lightweight service manager.

Perform the following steps:

1. Locate the source code at `/home/user/migration/backend.cpp`.
2. Update the C++ code so that it creates and binds to the Unix domain socket at exactly `/home/user/migration/run/app.sock` instead of its current legacy path.
3. Compile the updated source code using `g++` to an executable named `/home/user/migration/backend_server`.
4. Create the necessary `run` directory if it does not exist.
5. Create a watchdog bash script at `/home/user/migration/watchdog.sh`. The script must:
   - Check if the `backend_server` process is running.
   - If it is NOT running, delete any stale socket file at `/home/user/migration/run/app.sock`.
   - Start the `/home/user/migration/backend_server` process in the background.
6. Make the watchdog script executable.
7. Execute the watchdog script once manually so the service starts and the socket is created.
8. Create a file at `/home/user/migration/crontab.conf` that contains exactly one cron schedule line. This line should configure cron to run your `/home/user/migration/watchdog.sh` script every single minute. (You do not need to install it into the cron daemon, just write the valid crontab format line into this file).

Ensure the `backend_server` is running in the background and actively listening on the new socket path before you finish.
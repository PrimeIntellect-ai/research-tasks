You are a container specialist managing lightweight microservices in a custom Linux environment. We need to implement a simple C-based daemon and a lifecycle management script to act as a custom init/supervisor system for it, as we cannot use systemd inside these specific containers.

Your task is to create the microservice, its configuration, and its management script. 

Perform the following steps:

1. Create a configuration file at `/home/user/config.env` with exactly this content:
STATUS=RUNNING

2. Write a C program at `/home/user/heartbeat.c` that acts as the daemon. The program must:
- Include necessary headers for standard I/O, signals, and POSIX standard functions.
- Read `/home/user/config.env`. If the file does not contain `STATUS=RUNNING`, the program should exit immediately with code 1.
- Enter an infinite loop where it sleeps for 1 second at a time.
- Handle `SIGUSR1`: When received, append the exact text "Heartbeat received\n" to `/home/user/heartbeat.log`.
- Handle `SIGTERM`: When received, append the exact text "Shutting down\n" to `/home/user/heartbeat.log` and gracefully exit the program with code 0.
Make sure to flush file streams so logs appear immediately.

3. Compile the C program to an executable located at `/home/user/heartbeat`.

4. Write a bash script at `/home/user/svc.sh` that provides service lifecycle management. The script must accept exactly one argument (`start`, `stop`, or `ping`) and behave as follows:
- `./svc.sh start`: Starts `/home/user/heartbeat` in the background. It must write the background process's PID to `/home/user/heartbeat.pid`.
- `./svc.sh ping`: Reads the PID from `/home/user/heartbeat.pid` and sends a `SIGUSR1` signal to that process.
- `./svc.sh stop`: Reads the PID from `/home/user/heartbeat.pid`, sends a `SIGTERM` signal to that process, waits for the process to actually terminate, and then deletes the `/home/user/heartbeat.pid` file.

Make sure `/home/user/svc.sh` is executable. Do not start the service yourself; the automated testing suite will execute your script to verify the lifecycle.
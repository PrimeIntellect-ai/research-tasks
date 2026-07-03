You are a Linux systems engineer implementing a hardened health reporting mechanism. We want to avoid relying on external shell commands like `df` or `nc` in our monitoring scripts to reduce the attack surface. Instead, you need to build a standalone, compiled C utility that checks disk space and reports it directly over a TCP socket, configured purely via environment variables defined in a shell profile.

Perform the following tasks:

1. Create a directory named `/home/user/data_dir`. 

2. Write a C program at `/home/user/health_reporter.c` that does the following:
   - Reads the environment variables `REPORTER_HOST` and `REPORTER_PORT`.
   - Uses the POSIX `statvfs` API to determine the available free space (in bytes) of the `/home/user/data_dir` directory. Calculate this as `f_bavail * f_frsize`.
   - Creates a TCP socket and connects to the host and port specified by the environment variables.
   - Sends exactly this string over the socket: `DATA_DIR_FREE_BYTES:<bytes>\n` (where `<bytes>` is the integer value of the free space).
   - Closes the socket and exits with status 0. If any step fails (e.g., environment variables missing, directory not found, connection refused), it should print an error to standard error and exit with status 1.

3. Compile the C program to an executable at `/home/user/health_reporter` using `gcc` (e.g., `gcc -O2 /home/user/health_reporter.c -o /home/user/health_reporter`).

4. Append the necessary environment variable definitions to `/home/user/.bash_profile` so that any login shell has them. Specifically, export `REPORTER_HOST=127.0.0.1` and `REPORTER_PORT=8888`.

5. Create a wrapper script at `/home/user/run.sh` that explicitly sources `/home/user/.bash_profile` and then executes `/home/user/health_reporter`. Ensure the script has executable permissions.

Your solution will be verified by spinning up a dummy listener on port 8888, executing your `run.sh` wrapper, and verifying the exact formatted network payload received.
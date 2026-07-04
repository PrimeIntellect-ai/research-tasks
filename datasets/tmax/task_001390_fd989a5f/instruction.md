You are an infrastructure engineer debugging a custom C++ storage monitoring daemon that keeps failing to start in our staging environment. 

The source code for this daemon is vendored at `/app/storage-monitor-1.0`. It is designed to read a sequence of disk usage statistics and output formatting warnings. However, the service is currently failing. 

Your task is to:
1. Identify and fix a bug in the vendored package's `Makefile` and environment configuration that prevents it from compiling correctly. The build relies on an environment variable `STORAGE_ENV` which must be set to `STAGING`, but the Makefile has a typo preventing it from reading this properly.
2. Once compiled, you will notice the daemon crashes or produces incorrect output when parsing quota limits. You must debug and fix the C++ source code (`monitor.cpp`) so that its output is exactly equivalent to the expected behavior.
3. The daemon takes input from `stdin` (a stream of integers representing disk usage in MB) and should output `OK` if the usage is below 1024, `WARNING` if it is between 1024 and 2048, and `CRITICAL` if it is over 2048. Each output should be on a new line.
4. After fixing the code, compile it to an executable named `storage-daemon` and place it in `/home/user/bin/storage-daemon`.
5. Create a shell script at `/home/user/deploy.sh` that sets the correct environment variables and launches the daemon, simulating a staged deployment.

Ensure the final executable is perfectly accurate, as it will be rigorously tested against a reference implementation using randomized inputs.
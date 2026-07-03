You are a Site Reliability Engineer (SRE) configuring a lightweight uptime monitor for a QEMU Virtual Machine's VNC interface. You need to back up your current environment configuration, update your shell profile with a new monitoring target, and write a custom C++ checker to monitor the VNC port.

Perform the following tasks:

1. **Backup Strategy**: 
   Create a directory at `/home/user/backups`.
   Copy your current `/home/user/.bashrc` file to `/home/user/backups/bashrc.bak` to preserve the original configuration.

2. **Environment Variable Setup**: 
   Append an environment variable definition to `/home/user/.bashrc` that sets `SRE_MONITOR_PORT=5922`. This represents the target VNC port for the QEMU VM we want to monitor.

3. **Monitor Implementation (C++)**:
   Write a C++ program in `/home/user/uptime_checker.cpp` that does the following:
   - Reads the `SRE_MONITOR_PORT` environment variable. If the variable is not set, default to `5900`.
   - Attempts to establish a standard TCP connection to `127.0.0.1` on the specified port.
   - If the connection is successfully established, immediately close the socket and append the exact string `STATUS: VNC_UP\n` to the log file at `/home/user/sre_uptime.log`.
   - If the connection fails (e.g., connection refused), append the exact string `STATUS: VNC_DOWN\n` to `/home/user/sre_uptime.log`.

4. **Compilation**:
   Compile the C++ program into an executable named `/home/user/check_uptime`. Ensure there are no compilation errors.

(You do not need to run the executable yourself, but it must be fully functional and accurately detect open vs. closed ports when the testing suite executes it.)
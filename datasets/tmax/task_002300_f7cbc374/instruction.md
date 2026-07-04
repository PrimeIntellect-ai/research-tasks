A colleague is trying to deploy a new Go-based monitoring tool that connects to a local QEMU VNC instance. To ensure it will work correctly when deployed as a systemd service, they are testing it using a wrapper script (`/home/user/app/systemd_sim.sh`) that simulates systemd's clean environment by stripping out all environment variables before executing the binary.

Currently, the application fails to start when run through this script. We need you to diagnose the issue and get it running.

Your tasks are:
1. Examine the Go source code at `/home/user/app/vnc-monitor.go` to understand its startup requirements (it depends on specific locale, timezone, and network settings).
2. Compile the Go application to an executable named `/home/user/app/vnc-monitor`.
3. Create an environment file at `/home/user/app/monitor.env` that defines all necessary environment variables so the Go application can start successfully. The QEMU VNC server is running locally on VNC display `:1` (which corresponds to a specific TCP port).
4. Run the simulator script: `/home/user/app/systemd_sim.sh`. This script is already configured to read `/home/user/app/monitor.env` and pass its variables to the application, but the `.env` file currently does not exist.

Once successful, the application will automatically write a log file to `/home/user/app/status.log`. 

Ensure that `/home/user/app/status.log` is generated and contains the exact success string emitted by the Go application.
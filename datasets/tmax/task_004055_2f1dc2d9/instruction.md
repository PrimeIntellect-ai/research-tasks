You are a cloud architect preparing to migrate a legacy network service. To ensure the new infrastructure is ready, you need to build a mock migration service, set up its directory structure, and prepare its service lifecycle configurations.

Perform the following steps:

1. **Write the Mock Service in C++**: 
   Create a file at `/home/user/migrator.cpp`. The program must:
   - Read the `MIGRATION_PORT` and `MIGRATION_LOG` environment variables.
   - Bind and listen on a TCP socket at `127.0.0.1` using the port specified by `MIGRATION_PORT`.
   - Immediately after successfully entering the listening state, append the exact string `SERVICE_UP` followed by a newline to the file path specified by `MIGRATION_LOG`.
   - Enter an infinite loop (e.g., accepting connections or sleeping) so the process stays alive.

2. **Compile and Structure**:
   - Create the necessary directory structure: `/home/user/app/bin/`, `/home/user/app/active/`, and `/home/user/app/logs/`.
   - Compile the C++ program into the binary `/home/user/app/bin/migrator`.
   - Create a symbolic link at `/home/user/app/active/migrator` that points to `/home/user/app/bin/migrator`.

3. **Service Configuration (systemd)**:
   - Create a user-level systemd service file at `/home/user/.config/systemd/user/migrator.service`.
   - The service file must include a `[Service]` section that sets `ExecStart=/home/user/app/active/migrator`.
   - It must also use the `Environment` directive to set `MIGRATION_PORT=9090` and `MIGRATION_LOG=/home/user/app/logs/migrator.log`.

4. **Service Execution (Fallback Shell Script)**:
   Since the containerized environment may not have a running systemd instance for user services, write a robust startup script at `/home/user/app/start.sh` that:
   - Sets and exports `MIGRATION_PORT=9090` and `MIGRATION_LOG=/home/user/app/logs/migrator.log`.
   - Executes the symlinked binary (`/home/user/app/active/migrator`) in the background.
   - Saves the Process ID (PID) of the background process to `/home/user/app/migrator.pid`.
   - Make sure the script is executable.

5. **Start the Service**:
   - Execute `/home/user/app/start.sh` so the mock service is actively running and listening on the port.
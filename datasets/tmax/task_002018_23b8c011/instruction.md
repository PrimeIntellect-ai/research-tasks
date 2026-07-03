You are a site administrator managing a user account synchronization system. The application architecture simulates a microservice setup where a backend process (the User DB Service) and a worker process (the Sync Worker) communicate over local loopback interfaces. 

Currently, there is a severe network performance issue. The Sync Worker is successfully connecting to the User DB Service to synchronize user accounts, but the requests are unacceptably slow (taking over 0.5 seconds per request). This is causing a massive backlog in user account provisioning.

The system is set up in `/home/user/app/` with the following details:
1. The services are managed via Python scripts in `/home/user/app/services/`.
2. Both services run using a dedicated virtual environment located at `/home/user/app/venv`.
3. The virtual environment was built using a vendored, third-party networking library: `urllib3`. The source code for this vendored package is located at `/home/user/app/urllib3-src`.

Your tasks are to:
1. Diagnose the network performance issue. The root cause is a deliberate perturbation (a hardcoded delay for specific loopback IPs) injected into the vendored `urllib3` source code.
2. Fix the vendored source code to remove the artificial delay.
3. Reinstall the patched `urllib3` package into the `/home/user/app/venv` virtual environment.
4. Restart the Sync Worker process to apply the changes (ensure the DB service remains running or is restarted as well).
5. Create a symbolic link at `/home/user/app/latest_logs` that points to the `/home/user/app/services/logs` directory.

You do not have root access. You must use standard Linux terminal commands and Python to investigate and fix the issue. A successful fix will allow the synchronization of 20 accounts to complete in less than 1 second.
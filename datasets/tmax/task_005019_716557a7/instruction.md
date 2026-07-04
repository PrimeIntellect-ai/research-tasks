You are acting as a cloud architect migrating our legacy infrastructure to a new deployment model. Our old system relies on a proprietary routing component that maps user connection tokens to specific backend worker ports. We lost the source code for this legacy router, and we need to replace it with a clean C implementation before setting up our new reverse proxy.

Here is your multi-phase objective:

Phase 1: Reverse Engineering & Reimplementation (C)
We have recovered a stripped, UPX-packed binary of the legacy routing component located at `/app/legacy_router`. 
1. Analyze this binary. It takes a single command-line argument (a string token) and prints an integer (the backend port number) to standard output.
2. Write a new C program at `/home/user/new_router.c` that is functionally equivalent to the legacy binary. It must accept a single string argument and print the exact same port number as the legacy binary for any given token.
3. Compile your program to `/home/user/new_router`.

Phase 2: Environment and Reverse Proxy Setup
1. Set a persistent environment variable `ROUTER_MODE=migration` in the user's default shell profile (`/home/user/.bashrc`).
2. Write a lightweight Nginx configuration at `/home/user/proxy.conf` that acts as a reverse proxy, listening on port 9000 and load balancing across 4 backend ports (8080, 8081, 8082, 8083).

Phase 3: Interactive Automation & Backup
1. Write an Expect script at `/home/user/verify_deployment.exp` that simulates an interactive deployment check. It should spawn a pseudo-terminal running a hypothetical interactive tool (you can test against `/bin/bash` for now), export `ROUTER_MODE`, and test the compilation of `new_router.c`, expecting zero exit codes.
2. Write a bash script at `/home/user/backup_strategy.sh` that creates a tar.gz archive of `/home/user/proxy.conf` and `/home/user/new_router.c` into `/home/user/backups/deploy_backup.tar.gz`. The script should create the `backups` directory if it does not exist.

Ensure your C program is highly efficient and exactly matches the legacy binary's output, as it will be rigorously tested against random token inputs.
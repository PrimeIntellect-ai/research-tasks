I am an infrastructure engineer automating the provisioning and resilience of a lightweight, custom container architecture. In our system, "containers" are simulated as isolated directories containing state and data files. 

Currently, our system has several containers located in `/home/user/containers/`. Each container directory (e.g., `/home/user/containers/c1`, `/home/user/containers/c2`, etc.) contains two critical files:
1. `status.txt` - Contains either the string `HEALTHY` or `UNHEALTHY`.
2. `data.bin` - The persistent workload data for that container.

We maintain a backup of the data files in `/home/user/backups/`. The backup file for a container named `<id>` is stored as `/home/user/backups/<id>_data.bin`.

I need you to write a C++ health check and automated restore utility to manage this lifecycle.

Please do the following:
1. Write a C++ program at `/home/user/health_monitor.cpp`.
2. The program must iterate through all directories in `/home/user/containers/`.
3. For each directory, it should read the `status.txt` file.
4. If the status is `UNHEALTHY`, the program must perform a restore operation:
   - Overwrite the container's `data.bin` with the corresponding backup file from `/home/user/backups/<id>_data.bin`.
   - Update the container's `status.txt` to `HEALTHY`.
   - Append a log entry to `/home/user/health_monitor.log` exactly in this format: `RESTORED <id>` (followed by a newline), where `<id>` is the name of the container directory (e.g., `c2`).
5. Compile your program using `g++ -std=c++17 /home/user/health_monitor.cpp -o /home/user/health_monitor`.
6. Run the compiled `/home/user/health_monitor` executable.

Ensure your C++ code correctly uses standard libraries (like `<filesystem>` and `<fstream>`) and gracefully skips any directories that lack a `status.txt`. Do not hardcode the specific container names in your C++ file, as the environment may have dynamic container IDs.
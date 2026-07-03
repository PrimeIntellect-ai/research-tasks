I am a capacity planner, and I need your help setting up a reliable resource usage analysis pipeline. 

I have a proprietary, stripped binary located at `/app/bin/sys-profiler`. Because it is stripped and lacks documentation, I only know that it is an executable that analyzes system resource files. You will need to inspect it to determine how to run it (it expects certain command-line flags for a data directory and a port, and listens for a specific TCP payload to return capacity plans).

Your task is to write a Python process supervisor and API gateway in `/home/user/planner.py` that integrates this binary into a robust service.

Your Python script must:
1. **Directory & Link Management:** Create a base directory `/home/user/metrics/`. Every time the script starts, it should create a new timestamped subdirectory (e.g., `run_<timestamp>`) and update a symlink `/home/user/metrics/current` to point to it.
2. **Permissions:** Ensure the `/home/user/metrics/` directory and all contents have permissions set to `0700`.
3. **Process Supervision:** Spawn the `/app/bin/sys-profiler` subprocess, pointing its data directory argument to the `/home/user/metrics/current` symlink, and assigning it a local port of your choosing. If the profiler process crashes, your Python script must automatically restart it.
4. **API Gateway (Multi-Protocol):** The Python script must listen on `127.0.0.1:8080` (HTTP). 
   - `POST /metric` with a JSON body: Write the payload to a new file in the `current` metrics directory.
   - `GET /plan`: Send the proper trigger phrase (which you must reverse-engineer from the binary) over TCP to the `sys-profiler`'s port, and return its response directly to the HTTP client.
5. **Backup Strategy:** Before starting the new run, find any existing timestamped subdirectories in `/home/user/metrics/` that are older than the current run, compress them into a `.tar.gz` archive in `/home/user/backups/`, and delete the original subdirectories.

Run your script in the background so it is actively listening on `127.0.0.1:8080` when you complete the task. Do not use root privileges.
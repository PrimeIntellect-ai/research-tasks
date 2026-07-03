You are a container specialist managing a custom microservices architecture. Since you operate in an environment where true container runtimes (like Docker) are not available, you use a directory-based "pseudo-container" system and rolling shell scripts to manage deployments.

Your task is to write a C++ microservice worker, parse a deployment history file to find the correct version, set up simulated volume mounts via an fstab-like configuration, and write an automation script to deploy the service.

Phase 1: The C++ Microservice
Write a C++ program at `/home/user/src/worker.cpp` that acts as our service. The program must:
1. Accept exactly two command-line arguments: `version` (a string) and `mount_dir` (a path).
2. Read the first line of the file `config.txt` located inside `mount_dir`.
3. Open (in append mode) a file named `app.log` located inside `mount_dir`.
4. Write the following string to `app.log`: `<version> RUNNING <first_line_of_config>` followed by a newline.
5. Enter an infinite loop where it sleeps for 1 second at a time (to simulate a continuous background service).

Phase 2: Text Processing & Mount Configuration
You have two existing files on the system:
1. `/home/user/build_history.txt`: Contains build logs.
2. `/home/user/vmounts.fstab`: Contains volume mappings in the format `<source_dir> <target_dir> bind 0 0`.

Write a bash automation script at `/home/user/rollout.sh` that performs a staged deployment. The script must:
1. Parse `/home/user/build_history.txt` using tools like `awk`, `grep`, or `sed` to find the highest version number that has `status=SUCCESS`.
2. Parse `/home/user/vmounts.fstab` to find the source and target directories.
3. Simulate the mount by creating a symbolic link at `target_dir` that points to `source_dir`. (If `target_dir` already exists, remove it first).
4. Compile your `/home/user/src/worker.cpp` program using `g++` into an executable at `/home/user/bin/worker`.
5. Execute the compiled worker in the background, passing the version extracted from step 1 and the `target_dir` from step 2 as arguments.
6. Save the Process ID (PID) of the background worker to `/home/user/run/worker.pid`.

Finally, run your `/home/user/rollout.sh` script so the worker is actively running in the background.

Constraints & Assumptions:
- Ensure you create any missing directories (like `/home/user/src`, `/home/user/bin`, `/home/user/run`) before writing files to them.
- `/home/user/app_data/config.txt` already exists and contains configuration data.
- The `app.log` file will be verified automatically.
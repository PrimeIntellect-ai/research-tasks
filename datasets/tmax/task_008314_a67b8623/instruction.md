You are an infrastructure engineer setting up an automated deployment pipeline for a custom C++ provisioning daemon. Due to security restrictions, you cannot use root privileges, and the daemon requires interactive authentication on startup before it can begin serving. 

Your goal is to build the C++ daemon, create an interactive automation script using `expect`, create a simple process supervisor, and wrap it all in a continuous deployment script that handles staging and production rollouts.

All work should be done within `/home/user/provision_project`. Ensure you create this directory and the necessary subdirectories: `src`, `build`, `staging`, and `production`.

Please complete the following components:

1. **The C++ Daemon (`/home/user/provision_project/src/daemon.cpp`)**
   Write a C++ program that:
   - Prints exactly `Enter deployment key: ` to standard output.
   - Reads a string from standard input.
   - If the input matches exactly `PROV-SEC-99`, prints `INIT OK` and exits with status code `0`.
   - If the input does not match, prints `AUTH FAIL` and exits with status code `1`.

2. **The Expect Script (`/home/user/provision_project/test.exp`)**
   Write an `expect` script that automates the testing of this interactive prompt.
   - It should take the path to an executable as its first argument.
   - It should spawn the executable.
   - It must expect the prompt `Enter deployment key: `.
   - It must send the correct key (`PROV-SEC-99\r`).
   - It must expect `INIT OK`.
   - It must exit with the underlying process's exit code.

3. **The Process Supervisor (`/home/user/provision_project/supervisor.sh`)**
   Write a bash script that takes an executable path as its first argument and acts as a process supervisor.
   - It should run the executable.
   - If the executable exits with a non-zero exit code (e.g., failed authentication), the supervisor must print `RESTARTING` to stdout, and loop to run it again.
   - If the executable exits with a zero exit code (success), the supervisor must print `STOPPING` to stdout and exit.

4. **The CI/CD Pipeline (`/home/user/provision_project/pipeline.sh`)**
   Write a bash script that ties these together in a staged deployment:
   - Compile `src/daemon.cpp` using `g++` and output the binary to `build/daemon`.
   - Copy the compiled binary to `staging/daemon`.
   - Run the expect script against the staging binary: `./test.exp ./staging/daemon`.
   - Check the exit code of the expect script.
   - If the test is successful (exit code 0), roll out the deployment by copying the binary to `production/daemon`.
   - Lock down the production binary permissions so that it is read-and-execute ONLY for the owner (octal permission `500`), modifying ACL/permissions appropriately.
   - If the deployment succeeds to production, create a file `/home/user/provision_project/deploy_status.log` containing exactly the word `SUCCESS`.

Run your `pipeline.sh` script to perform the deployment and leave the final state ready for automated verification. Do not start the supervisor in the pipeline; we will test the supervisor independently.
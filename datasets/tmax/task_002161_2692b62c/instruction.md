You are managing a custom, lightweight "operator" written in C that processes deployment manifests. Currently, the operator fails to run because it cannot locate its network configuration file, simulating a scenario where service discovery fails due to environment misconfigurations. 

You have been given a workspace at `/home/user/operator_project` containing:
- `operator.c`: The source code for the operator.
- `network_config.json`: The network configuration file it needs to read.

Your task is to fix the environment setup and create a mini CI/CD deployment script that compiles and supervises the operator process.

Perform the following steps:
1. Create a shell profile file at `/home/user/operator_project/.env_profile`. This file must export the environment variable `NETWORK_CONFIG_PATH` set exactly to the absolute path `/home/user/operator_project/network_config.json`.
2. Create a bash script at `/home/user/operator_project/ci_cd.sh` that acts as a simple CI/CD and process supervisor. The script must:
    - Compile `/home/user/operator_project/operator.c` into an executable named `/home/user/operator_project/operator.bin` using `gcc`.
    - Source the `/home/user/operator_project/.env_profile` file to load the environment variable.
    - Implement a supervision loop: Run `/home/user/operator_project/operator.bin`. If the process exits with a non-zero status, restart it. It should attempt to run the process up to a maximum of 3 times. If the process exits with a status of `0`, the loop should terminate successfully immediately.
3. Make `ci_cd.sh` executable and run it.

If successful, `operator.bin` will read the configuration and automatically generate a log file at `/home/user/operator_project/deploy.log` containing a successful deployment message. Do not manually create `deploy.log` or modify `operator.c`.
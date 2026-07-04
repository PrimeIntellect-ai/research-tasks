You are tasked with fixing and deploying a custom local Kubernetes-style manifest generator (an "operator") written in C++.

Currently, the C++ code has a bug similar to a common reverse-proxy misconfiguration: it generates manifests with an incorrect upstream socket path, which causes downstream validation to fail (simulating a 502 bad gateway). Additionally, we need a robust, idempotent bash script to manage its execution and handle basic storage limits.

Here is your task:

1. **Fix the C++ Operator**
   You will find a source file at `/home/user/operator.cpp`. 
   It reads a configuration from `/home/user/input.conf` and outputs a YAML manifest to `/home/user/manifests/output.yaml`.
   Currently, it hardcodes the upstream socket path in the YAML output to `/home/user/sockets/upstream.sock`. 
   Modify the C++ code so that it instead writes the correct path: `/home/user/run/upstream.sock`.
   Compile your fixed code to an executable located at `/home/user/operator`.

2. **Create a Robust Wrapper Script**
   Write a bash script at `/home/user/sync_manifests.sh`. The script must:
   - Include `set -e` and `set -o pipefail` for robust error handling.
   - Be idempotent: safely create the directories `/home/user/manifests` and `/home/user/run` if they do not already exist.
   - Implement basic storage monitoring: Count the number of files in `/home/user/manifests/`. If there are strictly more than 3 files in this directory, delete all files in it that have the `.bak` extension.
   - Execute the compiled C++ operator (`/home/user/operator`).
   - Catch the exit code of the operator. If it succeeds (exit code 0), write exactly the string `SUCCESS` to `/home/user/sync_status.log`. If the operator fails, write exactly the string `FAILURE` to `/home/user/sync_status.log` and exit with code 1.

Ensure `/home/user/sync_manifests.sh` is executable (`chmod +x`). 
Run your script once to ensure `/home/user/manifests/output.yaml` is generated correctly and `/home/user/sync_status.log` reads `SUCCESS`.
You are tasked with building a simulated GitOps Kubernetes Operator using Python and Git hooks. You will configure a local Git repository, write a post-receive hook, and build a Python script that acts as our "operator" by managing environment profiles, system state configs, and container lifecycle simulation scripts.

Complete the following steps:

1. **Git Repository Setup**:
   - Create a bare Git repository at `/home/user/manifest-repo.git`.
   - Create a local clone of this repository at `/home/user/manifest-workspace`.

2. **The Operator Script**:
   - Write a Python script at `/home/user/operator.py`. Ensure it is executable.
   - This script will be executed by a Git hook every time new commits are pushed to `manifest-repo.git`.
   - The script must read the latest pushed state of the repository (you can use `git archive` or similar commands to extract the latest `master` branch to a temporary directory inside the Python script).
   - The script must search for all `.yaml` files in the root of the repository. Each file represents a deployment manifest with the following exact structure:
     ```yaml
     name: <string>
     image: <string>
     replicas: <integer>
     env:
       <key>: <value>
     ```
   - **State Configuration**: Parse all found YAML files and write their collective state to a single JSON file at `/home/user/cluster_state.json`. The JSON must be a dictionary where the keys are the `name` of each deployment, and the values are the full dictionaries from the parsed YAMLs.
   - **Environment Profile setup**: For every environment variable defined in every deployment, append an export statement to `/home/user/.k8s_profile` in the format: `export K8S_ENV_<NAME_IN_UPPERCASE>_<ENV_KEY>="<ENV_VALUE>"`. (Overwrite the file from scratch on each run).
   - **Container Lifecycle Simulation**: Generate a robust bash script at `/home/user/apply_containers.sh`. This bash script must:
     - Start with `set -eo pipefail`.
     - For each deployment, and for each replica (from `1` to `replicas`), append a command to the bash script that echoes the following exact string into `/home/user/container.log`:
       `Starting container [image] for deployment [name] (replica [N]) with env keys: [comma_separated_env_keys]`
       *(Example: `Starting container nginx:1.19 for deployment frontend (replica 1) with env keys: PORT,DEBUG`)*

3. **Git Hook Configuration**:
   - Create a `post-receive` hook in `/home/user/manifest-repo.git/hooks/post-receive`.
   - Make it executable.
   - The hook must simply execute `/home/user/operator.py` whenever a push is received.

4. **Testing the Pipeline**:
   - Inside `/home/user/manifest-workspace`, create a file named `backend.yaml` with the following content:
     ```yaml
     name: backend-api
     image: python:3.9-slim
     replicas: 2
     env:
       PORT: 8080
       DB_HOST: pg-cluster.local
     ```
   - Commit this file to the `master` branch and push it to the bare repository (`origin`).
   - If your setup is correct, the push will trigger the hook, run the Python script, generate the configs, and create `/home/user/apply_containers.sh`.
   - Finally, execute `/home/user/apply_containers.sh` manually from the terminal.

Constraints:
- Do not use root privileges (no `sudo`).
- You may install the `pyyaml` package using `pip install pyyaml` if needed.
- All file paths must be exactly as specified.
You need to fix a local mock Kubernetes operator environment that manages application manifests. The system consists of an interactive configuration wizard, a directory structure of YAML manifests, and a custom process runner. 

Perform the following tasks:

1. **Interactive Configuration (Expect Scripting):**
   There is an interactive bash script at `/home/user/setup_wizard.sh`. It prompts for two values:
   - `Enter environment:` (You must answer `production`)
   - `Enter manifest dir:` (You must answer `/home/user/manifests/active`)
   Write a Python script at `/home/user/configure.py` that programmatically interacts with this bash script (you may use the `pexpect` library, which you can install via `pip install pexpect`). Running your Python script must successfully complete the wizard, which will generate `/home/user/operator.conf`.

2. **Filesystem and Link Management:**
   The operator only manages Deployments. Read all `.yaml` files in `/home/user/manifests/available/`. 
   Create the directory `/home/user/manifests/active/`. 
   For every YAML file in the `available` directory that contains the exact line `kind: Deployment`, create a symbolic link to it inside `/home/user/manifests/active/` with the exact same filename.

3. **Process Dependency Fix:**
   The mock operator and its manifest validator are managed by a custom process runner using the configuration file `/home/user/services.json`.
   Currently, the `operator` service fails to start because it attempts to run before the `validator` service has initialized (similar to a missing `After=` systemd directive).
   Modify `/home/user/services.json` and add a `"depends_on": "validator"` key-value pair to the `operator` service configuration block so that the runner knows to start the validator first.

4. **Execution:**
   Once the above steps are complete, run the Python script `/home/user/runner.py`. 
   If everything is configured correctly, it will validate the manifests, boot the operator, and generate a final log file at `/home/user/operator_success.log`.
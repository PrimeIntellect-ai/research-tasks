You are tasked with fixing and securing our user account provisioning pipeline. We manage lightweight user environments where users submit their SSH keys and cron schedules via Git. A vendored python tool processes these, but it is currently broken, and our submission system lacks security validation.

**Step 1: Fix the Vendored Provisioning Tool**
We use a custom tool called `vm-user-sync`. Its source is vendored at `/app/vm-user-sync-1.0.0`.
Currently, the package cannot be built or run due to two issues:
1. The `Makefile` used to build the python wheel has a deliberate perturbation (spaces instead of tabs) causing `make build` to fail.
2. The systemd template used by the tool to schedule tasks (`vm_user_sync/templates/user-service.jinja`) is failing our infrastructure linters because it is missing a critical startup dependency. It must wait for the network to be online. You must add `After=network.target` to the `[Unit]` section.

Fix the package, build it, create a Python virtual environment at `/home/user/venv`, and install the fixed package into this environment.

**Step 2: Create a Configuration Validator**
Users submit configurations, but some are malicious. Write a Python script at `/home/user/validator.py` that takes a single argument: the path to a user's configuration directory.
The script must analyze the directory and exit with `0` (clean) or `1` (malicious/invalid).
A directory is malicious if ANY of the following are true:
- Symlink Escape: Any symbolic link in the directory resolves to a path outside of the provided directory path.
- Malicious SSH keys: Any file ending in `.ssh_key` contains the string `command=` (often used to force command execution on SSH login).
- Dangerous Cron Jobs: Any file ending in `.cron` contains any of the following restricted commands in the file: `curl`, `wget`, `nc`, or `bash`.

**Step 3: Setup the Git Repository and Hook**
1. Initialize a bare Git repository at `/home/user/provisioning.git`.
2. Create a `pre-receive` hook in this repository that reads the incoming tree. However, since parsing Git trees in a hook can be complex, for this task, the hook only needs to exist, be executable, and contain a placeholder comment `# VALIDATOR_INTEGRATION_READY`.

Test your validator script against the test corpora located at `/app/corpus/clean/` and `/app/corpus/evil/`. Every subdirectory in `/app/corpus/clean/` must return `0`, and every subdirectory in `/app/corpus/evil/` must return `1`.
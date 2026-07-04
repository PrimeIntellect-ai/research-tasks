You are a network engineer troubleshooting and securing a local Virtual Machine deployment platform. We use a custom tool to generate QEMU network configurations and filesystem mounts, but our deployment pipeline is currently broken and vulnerable to path traversal attacks.

You have three main objectives:

**Part 1: Fix and Install the Vendored Package**
We have a custom Python package pre-vendored at `/app/vendored/qemu-net-builder`. This package manages QEMU network topologies. However, a recent commit introduced a perturbation that breaks the package.
1. Inspect the source code in `/app/vendored/qemu-net-builder`. You will find a deliberate bug in `qemu_net_builder/utils.py` that causes a type error during network generation.
2. Fix the bug.
3. Install the package into the current user's environment so that the `qemu-net-builder` CLI command is available in the user's PATH (e.g., using `pip install -e .` or similar in a virtual environment, or simply ensuring it can run).

**Part 2: Build a Security Validator (Adversarial Corpus)**
Users submit JSON configuration files for their QEMU VMs. These configurations specify a `"host_mount"` directory that will be shared with the VM. The base directory for all VM storage is strictly `/home/user/vm_storage/`. 

Malicious users are submitting configs trying to mount directories outside of `/home/user/vm_storage/` using path traversal (`../`) or tricky symlinks.
Write a Python script at `/home/user/validate_configs.py` that takes a single file path as a CLI argument:
`python3 /home/user/validate_configs.py <path_to_json>`

The JSON file has the format:
```json
{
  "vm_name": "test-vm",
  "host_mount": "my_folder/data"
}
```
The `host_mount` value is a relative path intended to be appended to `/home/user/vm_storage/`.
Your script must:
1. Parse the JSON.
2. Resolve the absolute, canonical path of the combined `/home/user/vm_storage/` + `host_mount`. It MUST correctly resolve any symlinks present on the filesystem.
3. Check if the final resolved directory is strictly a child (or the same directory) of the canonicalized `/home/user/vm_storage/`.
4. If it is safe (within the storage directory), exit with status code `0`.
5. If it is malicious (escapes the storage directory), exit with status code `1`.

**Part 3: Systemd Service Configuration**
Create a systemd user service file at `/home/user/.config/systemd/user/qemu-net-validator.service`. 
It should have:
- `Description=QEMU Net Validator`
- `ExecStart=/usr/bin/python3 /home/user/validate_configs.py /home/user/default_config.json`
- `Restart=on-failure`

You do not need to start or enable the service, just create the valid service file with the exact directory structure.
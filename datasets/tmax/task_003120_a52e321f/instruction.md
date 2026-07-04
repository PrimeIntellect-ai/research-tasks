You are acting as a capacity planner for a simulated virtualization fleet. Your objective is to analyze current resource usage from system logs, enforce capacity guardrails via Git hooks, and automate a staged deployment configuration. 

You must complete the following phases. All scripts and operations should take place in `/home/user`.

**Phase 1: Capacity Analysis via Text Processing**
You have two files representing the current state of the fleet:
1. `/home/user/net_status.txt`: Contains connectivity diagnostic logs. Format: `<vm_name> - <status>`. Status can be `REACHABLE` or `TIMEOUT`.
2. `/home/user/qemu_procs.txt`: Contains mock `ps` output for running QEMU virtualization processes. Each line shows the command used to start a VM, which includes the VM name (`-name <vm_name>`), RAM allocated (`-m <megabytes>`), and CPU cores (`-smp <cores>`).

Write a pipeline or Python script to calculate the total active resources. Only include VMs that are `REACHABLE` in `net_status.txt` AND present in `qemu_procs.txt`.
Write the final calculated totals to `/home/user/active_capacity.txt` strictly in this exact format:
```
ACTIVE_CPU: <total_cores>
ACTIVE_RAM: <total_megabytes>
```

**Phase 2: Git Server Hook Configuration**
There is a local bare Git repository at `/home/user/infra.git` representing the central infrastructure-as-code repository. Developers push changes to a file named `vms.json` to allocate new VMs.
You must create a Git `pre-receive` hook at `/home/user/infra.git/hooks/pre-receive`. The hook MUST be written in **Python**.
Requirements for the `pre-receive` hook:
- Read the incoming push (reading the standard input provided by Git `pre-receive` which is `<old_value> <new_value> <ref_name>`).
- Extract the contents of `vms.json` from the incoming commit. `vms.json` is a list of dictionaries, e.g., `[{"name": "new1", "cpu": 4, "ram": 8192, "env": "dev"}]`.
- Calculate the total CPU and RAM requested in the incoming `vms.json`.
- Read the current active usage from `/home/user/active_capacity.txt`.
- Add the incoming requested resources to the active resources.
- If the new total CPU exceeds 200 OR the new total RAM exceeds 512000 (MB), the hook must print an error message starting with "CAPACITY EXCEEDED" to stderr and exit with a non-zero status to reject the push.
- Otherwise, exit with status 0.
Make sure the hook is executable!

**Phase 3: Staged Deployment Script**
Write a deployment script at `/home/user/roll_deploy.py`. The script should:
- Accept a single argument: the path to a JSON file (e.g., `vms.json`).
- Parse the JSON array.
- Create two directories if they don't exist: `/home/user/deployments/stage_1` and `/home/user/deployments/stage_2`.
- For each VM in the JSON array:
  - If `"env": "dev"`, create a file `/home/user/deployments/stage_1/<vm_name>.conf` containing the string `cpu=<cpu>,ram=<ram>`.
  - If `"env": "prod"`, create a file `/home/user/deployments/stage_2/<vm_name>.conf` containing the string `cpu=<cpu>,ram=<ram>`.
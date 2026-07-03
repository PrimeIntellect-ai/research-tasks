You are a FinOps analyst tasked with automating the local extraction of cost telemetry from a mocked cloud virtualization environment. This environment helps simulate instance pricing before deploying real spot instances.

Currently, the orchestration process fails because the data extraction script attempts to connect before the emulator has fully initialized its services (a classic missing dependency issue). Your task is to build a robust bash orchestrator and an Expect script to reliably handle this lifecycle.

You need to perform the following steps:

1. **Directory and Link Management:**
   Write a script `/home/user/run_cost_analysis.sh` that first sets up the correct directory structure.
   - Create directories `/home/user/var/log/finops` and `/home/user/var/data/finops`.
   - Create a directory `/home/user/finops`.
   - Create symbolic links inside `/home/user/finops`:
     - `/home/user/finops/logs` pointing to `/home/user/var/log/finops`
     - `/home/user/finops/data` pointing to `/home/user/var/data/finops`

2. **Container/Service Lifecycle & Connectivity Diagnostics:**
   Inside `/home/user/run_cost_analysis.sh`, start the emulator daemon provided at `/home/user/cloud_emulator.sh` in the background. This daemon simulates a VM booting and eventually opens TCP port `8080`.
   - Capture the PID of this background process.
   - Implement a polling loop (using standard bash tools like `/dev/tcp` or `nc`) to check `localhost` on port `8080`. The script must wait until the port is open and accepting connections before proceeding. Do not hardcode a blind `sleep`—you must actively check for connectivity.

3. **Expect Scripting for Interactive Automation:**
   Create an Expect script at `/home/user/fetch_metrics.exp`.
   This script must:
   - Spawn the interactive mock SSH tool: `/home/user/cloud_ssh_mock`
   - Wait for the prompt: `Password: `
   - Send the password: `finops2024`
   - Wait for the prompt: `Emulator> `
   - Send the command: `fetch_cost`
   - Wait for the prompt: `Emulator> `
   - Send the command: `exit`
   
   Update `/home/user/run_cost_analysis.sh` to execute `/home/user/fetch_metrics.exp` immediately after the connectivity diagnostic confirms port 8080 is open. The orchestrator must redirect the standard output of the Expect script to `/home/user/finops/logs/cost.log`.

4. **Cleanup:**
   After the Expect script finishes, `/home/user/run_cost_analysis.sh` must gracefully terminate the background `cloud_emulator.sh` process (using the PID captured earlier) so no zombie processes are left listening on port 8080.

**Constraints:**
- Use Bash as your primary language for the orchestrator.
- Do not use root privileges (`sudo`).
- Ensure `run_cost_analysis.sh` and `fetch_metrics.exp` are executable (`chmod +x`).
- Your final deliverable is running `/home/user/run_cost_analysis.sh` successfully, resulting in the populated log file and a clean process tree.
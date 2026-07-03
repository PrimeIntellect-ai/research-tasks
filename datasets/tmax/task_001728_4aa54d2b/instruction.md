You are a FinOps analyst tasked with automating cloud cost optimization. We have a proprietary command-line tool that manages our container infrastructure, but it lacks bulk operations and requires interactive prompts, making it hard to use in our CI/CD pipelines.

Your task is to build a Bash-based automated pipeline script (`/home/user/cost_pipeline.sh`) that integrates with this tool to identify and shut down expensive, underutilized containers.

**Environment Details:**
- The CLI tool is located at `/home/user/cloud-manager`.
- The tool manages the container lifecycle but requires interactive inputs for sensitive actions.

**Tool Commands & Behavior:**
1. `/home/user/cloud-manager login`
   - Prompts interactively for `Username: ` and `Password: `.
   - Credentials to use: Username is `finops_admin` and Password is `CostSave2023!`.
   - On success, it creates a local session. You MUST login before running other commands.

2. `/home/user/cloud-manager list`
   - Outputs a CSV of currently running containers with the header:
     `ContainerID,CostPerHr,CPU_Percent,Mem_Percent`
   - Example output row: `C-999,4.50,2,5`

3. `/home/user/cloud-manager terminate <ContainerID>`
   - Interactively prompts: `Are you sure you want to terminate <ContainerID>? [y/N]: `
   - You must pass exactly `y` to confirm.
   - Outputs `Terminated <ContainerID>` on success.

**Pipeline Requirements:**
Write a script at `/home/user/cost_pipeline.sh` that automates the following CI/CD sequence:
1. Uses `expect` (or similar automation) to log in to `cloud-manager`.
2. Fetches the current list of running containers.
3. Identifies containers that meet **ALL** of the following "Wasteful" criteria:
   - `CostPerHr` is strictly greater than `2.00`.
   - `CPU_Percent` is strictly less than `5`.
   - `Mem_Percent` is strictly less than `10`.
4. Uses `expect` to interactively terminate the identified wasteful containers.
5. Writes the `ContainerID` of every successfully terminated container to `/home/user/terminated_containers.txt`, with one ID per line.

Once you have created `/home/user/cost_pipeline.sh`, execute it to ensure it processes the current environment correctly and creates the `/home/user/terminated_containers.txt` file. Make sure your script has execute permissions.
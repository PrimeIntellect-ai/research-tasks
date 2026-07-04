You are a FinOps analyst at a company trying to automate cloud cost governance. The company relies on a proprietary, legacy binary that calculates cloud deployment costs based on current vendor pricing. Unfortunately, this binary only runs interactively and lacks an API. 

Your objective is to wrap this binary in an automated pipeline to prevent developers from deploying infrastructure that exceeds a $500 budget.

1. **Expect Wrapper**
The legacy binary is located at `/app/bin/calc_cost`. When executed, it prints a welcome banner, prompts `Enter Region (us-east, eu-west): `, waits for input, then prompts `Enter Number of Instances: `, waits for input, and finally outputs `Total Estimated Cost: $<value>`.
Write an `expect` script at `/home/user/cost_wrapper.exp` that takes exactly two arguments (Region and Number of Instances), interacts with `/app/bin/calc_cost`, and prints **only** the numerical cost value (e.g., `150`) to standard output.

2. **Cost Daemon**
Write a Bash script at `/home/user/cost_api.sh` that acts as a simple TCP server listening on port `9000`. You must use `socat` or `nc` to listen on `127.0.0.1:9000`. 
For each incoming connection, the daemon must read a single line of text formatted exactly as `<region> <instances>` (e.g., `us-east 10`), pass these values to your `cost_wrapper.exp` script, and send the numerical cost back to the client over the TCP connection, followed by a newline.

3. **Process Supervision**
Write a supervisor script in Bash at `/home/user/supervisor.sh` that launches `cost_api.sh`, monitors its process, and automatically restarts it if it crashes or terminates. Execute your supervisor script in the background so the daemon is actively running and ready to accept connections.

4. **Git Hook Enforcement**
Initialize a bare Git repository at `/home/user/infra.git`.
Create a `pre-receive` hook in this repository that enforces our budget policy. 
When developers push code, they will be pushing a file named `deployment.conf` in the root directory. This file will contain a single line formatted as `<region> <instances>` (e.g., `eu-west 5`).
Your `pre-receive` hook must:
* Extract the contents of `deployment.conf` from the incoming commit.
* Send the extracted line to your Cost Daemon running at `127.0.0.1:9000` via TCP.
* Read the returned cost.
* If the cost is greater than 500, the hook must print `FinOps: Budget exceeded` to stderr and exit with code 1 (rejecting the push).
* If the cost is 500 or less, the hook must exit with code 0.

Ensure all scripts have the correct execution permissions and your daemon is running in the background when you complete your task.
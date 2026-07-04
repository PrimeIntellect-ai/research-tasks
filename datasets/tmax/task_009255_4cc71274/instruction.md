You are tasked with automating a legacy interactive deployment process using Go. 

There is an existing interactive shell script located at `/home/user/legacy-deploy.sh`. This script simulates deploying a service to a specific stage. It prompts the user for two inputs sequentially:
1. `Target environment (alpha/beta/prod): `
2. `Confirm deployment to <env> (yes/no): `

Your objective is to write a Go program at `/home/user/rollout.go` that acts as an "expect" script to automate this interactive process for a staged rolling deployment to the "beta" environment, while ensuring the operation is idempotent.

Requirements for `/home/user/rollout.go`:
1. **Idempotency**: At the very beginning of execution, the program must check if the file `/home/user/rollout.state` contains the exact string `SUCCESS_beta`. If it does, the program should print "Already deployed" and exit immediately with status code 0, without executing the bash script.
2. **Interactive Automation**: If the state file does not contain `SUCCESS_beta`, the Go program must execute `/home/user/legacy-deploy.sh`.
3. It must read the standard output of the script. 
4. When it detects the prompt `Target environment (alpha/beta/prod): `, it must write `beta\n` to the script's standard input.
5. When it detects the prompt `Confirm deployment to beta (yes/no): `, it must write `yes\n` to the standard input.
6. **State Tracking**: After the script finishes executing successfully (exit code 0), your Go program must create or overwrite `/home/user/rollout.state` with the exact string `SUCCESS_beta`.

Constraints:
- Use only the standard Go library (no third-party expect libraries like `goexpect`).
- Make sure your Go program handles the I/O streams correctly to prevent deadlocks.
- The Go file must compile successfully.
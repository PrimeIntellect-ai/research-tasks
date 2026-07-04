You are a deployment engineer rolling out a new resilient worker service. The deployment process requires interacting with a legacy vault system to fetch credentials, building a Rust-based worker that simulates intermittent failures, and wrapping it in a custom Bash supervisor.

Your tasks are to set up this deployment pipeline entirely within `/home/user/`:

1. **Automate the Vault (Expect Scripting)**
   There is a pre-existing script at `/home/user/vault_cli.py` which simulates a secret vault. When executed, it interactively prompts: `Enter deployment passphrase: `. 
   The passphrase is `deploy_2024`. 
   Write an Expect script named `/home/user/fetch_token.exp` that executes `/home/user/vault_cli.py`, provides the passphrase, and writes the successful output (a token string) into a new file `/home/user/config.env`.

2. **Write the Worker (Rust)**
   Write a Rust application in `/home/user/worker.rs`. The program must:
   - Read `/home/user/config.env` and verify it contains the string `TOKEN=ZGVwbG95X3NlY3JldA==`. If it doesn't, exit immediately with code `2`.
   - Check if the file `/home/user/crash.lock` exists.
   - If `/home/user/crash.lock` does **not** exist: Create the file `/home/user/crash.lock`, print `CRASHING` to stdout, and exit with code `1` (simulating a transient failure).
   - If `/home/user/crash.lock` **does** exist: Print `SUCCESS` to stdout, and exit with code `0`.
   
   Compile this program using `rustc /home/user/worker.rs -o /home/user/worker`. Ensure the compiled `/home/user/worker` executable has its permissions set to exactly `700` (read, write, execute for the owner only).

3. **Process Supervision (Bash)**
   Write a supervisor script at `/home/user/supervisor.sh` that ensures our unstable worker eventually succeeds. The script must:
   - Run `/home/user/worker` in a loop.
   - After each execution of the worker, append a line exactly matching `Worker exited with X` (where X is the actual exit code) to `/home/user/supervisor.log`.
   - If the worker exits with code `0`, the supervisor loop must break and the script should cleanly terminate.
   - If the worker exits with a non-zero code, the loop must continue and run the worker again.
   - Ensure `/home/user/supervisor.sh` has its permissions set to exactly `700`.

4. **Execute the Deployment**
   Finally, execute `/home/user/fetch_token.exp` to generate the config file, and then run `/home/user/supervisor.sh` to start the deployment and supervision process. Ensure `/home/user/supervisor.log` contains the final results.
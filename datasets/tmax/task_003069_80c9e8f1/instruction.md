You are tasked with building a custom service manager and rolling deployment tool in Rust for a mock mailing list server infrastructure. Since you do not have root access, you will orchestrate the service lifecycle at the user level, managing environment variables, configurations, and staged process execution.

Your goal is to complete the following requirements:

1. **Environment Setup**:
   Create a file at `/home/user/mail_env.sh` that exports the following environment variables:
   - `MAILING_DOMAIN=system-deploy.local`
   - `DEPLOY_WORKERS=3`
   - `ROLLOUT_DELAY_MS=100`

2. **Task Automation Script**:
   Create a shell script at `/home/user/mail_worker.sh` that simulates an email processing daemon. The script must:
   - Accept exactly one argument: the worker ID (e.g., 1, 2, or 3).
   - Read the `MAILING_DOMAIN` environment variable.
   - Append the exact string `[INIT] Worker <ID> listening for <MAILING_DOMAIN>` to the file `/home/user/worker_events.log`.
   - Exit with a status code of 0.
   Make sure the script is executable.

3. **Rust Lifecycle Manager**:
   Initialize a new Rust binary project at `/home/user/deployd`.
   Write a Rust program in this project that acts as the service manager. The Rust program must do the following:
   - Load the environment variables from `/home/user/mail_env.sh` (you may parse the file or assume the Rust process is run in an environment where they are already sourced, but your final test must run the binary).
   - Generate a mailing list configuration file at `/home/user/postfix_mock.cf` containing exactly two lines:
     `primary_domain = system-deploy.local`
     `active_daemons = 3`
   - Implement a **staged rolling deployment**:
     For each worker ID from 1 up to `DEPLOY_WORKERS` (inclusive):
     a. Spawn the `/home/user/mail_worker.sh` script as a child process, passing the current worker ID as the argument.
     b. Wait for the child process to exit successfully.
     c. Log the exact string `Staged rollout complete for worker <ID>` to `/home/user/deployd.log`.
     d. Sleep for `ROLLOUT_DELAY_MS` milliseconds before starting the next worker (use standard Rust thread sleeping).

4. **Execution**:
   Compile your Rust project (`cargo build --release`). 
   Run your compiled binary so that all the files (`postfix_mock.cf`, `worker_events.log`, and `deployd.log`) are generated and populated correctly.

Ensure all paths and log formats strictly match the instructions, as an automated system will verify the presence and exact contents of `/home/user/postfix_mock.cf`, `/home/user/worker_events.log`, and `/home/user/deployd.log`.
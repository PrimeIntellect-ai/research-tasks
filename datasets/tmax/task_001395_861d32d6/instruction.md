You are an administrator for a system that automates the deployment of user accounts. A previous administrator left the system in a broken state. You need to fix a vendored dependency, write a robust input sanitiser for user creation requests, and fix a scheduled cron job that runs the pipeline.

**Phase 1: Fix and Install the Vendored Dependency**
We rely on the `pexpect` library to interactively interface with a legacy user-creation daemon. The source code for `pexpect-4.8.0` is vendored at `/app/pexpect-4.8.0/`.
However, the previous administrator made a deliberate, hacky modification to its `setup.py` that currently prevents it from installing. 
1. Locate the perturbation in `/app/pexpect-4.8.0/setup.py` (a broken environment variable check or syntax error deliberately introduced to stop builds without a specific flag) and fix it.
2. Install the package locally into a virtual environment located at `/home/user/venv`. (Do not attempt to contact PyPI, do this entirely offline).

**Phase 2: Build the Account Request Sanitiser**
User account requests are dropped as JSON files. You must write a Python script at `/home/user/sanitise_users.py` that acts as a filter.
The script must take two CLI arguments:
`python /home/user/sanitise_users.py <input_json> <output_json>`

The input JSON is a list of dictionaries, where each dictionary represents a user request with keys: `username`, `home_dir`, and `shell`.
Your script must evaluate each request and ONLY write valid, safe requests to `<output_json>` (as a JSON list). A request must be REJECTED (dropped from the output) if:
- `username` contains characters other than lowercase alphanumeric, dashes, or underscores.
- `username` is longer than 32 characters.
- `home_dir` attempts directory traversal (e.g., contains `../` or `..\\`) or does not start with `/home/`.
- `shell` is not one of `/bin/bash`, `/bin/sh`, or `/usr/bin/zsh`.

We will test your script against a hidden corpus of "clean" and "evil" JSON payloads to ensure it perfectly drops malicious inputs and perfectly preserves valid ones.

**Phase 3: Automated Scheduling and Context Fixes**
There is a cron job designed to run an orchestrator script (`/home/user/orchestrator.py`) every minute. The cron job is defined in `/home/user/sync_cron` but is currently failing to write outputs correctly because it assumes environment variables (like `PATH` and `PWD`) that are present in interactive shells but missing in the cron environment.
1. Fix the cron configuration file at `/home/user/sync_cron` so that the scheduled job executes the orchestrator using your virtual environment's Python, and writes its log file explicitly to `/home/user/account_sync/output/sync.log` instead of implicitly writing to the wrong relative location.
2. Ensure `/home/user/account_sync/output/` exists and has permissions set to `0755` (ACL/Permission management).
3. Load the corrected cron job into the user's crontab.

Your final success will be evaluated by triggering the cron job, verifying that the log file is generated in the exact correct path, verifying the vendored `pexpect` package imports cleanly in your virtual environment, and running your `sanitise_users.py` script against our grading corpora.
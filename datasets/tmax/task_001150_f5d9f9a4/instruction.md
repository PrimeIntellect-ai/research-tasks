You are a deployment engineer tasked with migrating our legacy staging environment to a new Python-based microservice architecture. Currently, inter-service communication is failing because the new Python services cannot generate the correct authorization headers expected by the legacy router. 

There are two distinct parts to your task:

**Part 1: Automate the Staged Rollout**
We have an interactive bash script at `/app/legacy_deploy.sh` that stages the rollout of our worker nodes. Because it is interactive, it disrupts our CI/CD pipeline. 
Write a Python script at `/home/user/auto_deploy.py` that uses the `pexpect` module to completely automate the execution of `/app/legacy_deploy.sh`. 
The legacy script will prompt for the following configuration. You must provide exactly these answers:
- Target deployment tier: `staging`
- System timezone for logs: `Europe/Berlin`
- Expected system locale: `de_DE.UTF-8`
- Proceed with rolling restart? `yes`

*Note: You must ensure that your Python script sets the `TZ` and `LANG` environment variables to the above values before invoking the legacy deploy script, as the script verifies the environment before proceeding.*

**Part 2: Reimplement the Auth Signer (Reverse Engineering)**
Our system relies on a legacy C application located at `/app/auth_signer`. This is a stripped binary that takes a Unix timestamp (integer) as a single command-line argument and prints a localized maintenance window string to standard output. 
Because we are deprecating the C utilities, you must write a Python equivalent at `/home/user/auth_signer.py`. 

Your Python script must:
1. Accept exactly one command-line argument: a Unix timestamp (integer).
2. Produce output that is **bit-exact equivalent** to the output of `/app/auth_signer` for any valid integer input between `1600000000` and `1800000000`.
3. Account for Daylight Saving Time rules implicitly required by the binary.

You are expected to use black-box testing (and tools like `objdump` or `strings` if necessary) on `/app/auth_signer` to deduce the exact string formatting and timezone logic it uses.

**Acceptance Criteria:**
- `/home/user/auto_deploy.py` runs successfully and causes the legacy deploy script to emit its "Deployment successful" success message.
- `/home/user/auth_signer.py` precisely matches the output of `/app/auth_signer` for thousands of random timestamp inputs. 

Do not install any external Python packages other than `pexpect` (which is already available or can be installed via `pip install pexpect --user`).
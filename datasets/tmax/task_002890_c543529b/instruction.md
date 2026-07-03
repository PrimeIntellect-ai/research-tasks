You are a deployment engineer tasked with rolling out an update to our internal container provisioning pipeline. Recently, our storage systems have been experiencing severe disk quota abuses and instability because users are submitting malicious or malformed container deployment specifications. 

The core of our provisioning system relies on a legacy, proprietary system daemon that validates container specs. The validator binary is located at `/app/provision_validator` (it is a stripped, UPX-packed executable). Unfortunately, the source code for this binary is lost, but we know it processes configuration files and enforces disk quotas, mounts, and limits. However, it contains parsing vulnerabilities that bad actors are exploiting to bypass quotas or crash the container runtime system.

We have collected two corpora of deployment configuration files:
1. `/home/user/configs/clean/`: Contains 50 valid, normal configuration files that the legacy binary processes safely. We MUST allow these to be provisioned.
2. `/home/user/configs/evil/`: Contains 50 malicious or exploiting configuration files that trigger bypasses or crashes in the legacy binary. We MUST block these.

Your task is to create a Python-based pre-flight filter that will act as a sanitizer in our deployment pipeline.

Requirements:
1. **Analyze the legacy binary**: Use reverse engineering tools (like `strings`, `objdump`, or `strace` while feeding it test files) or treat it as a black box against the corpora to determine exactly what patterns, values, or anomalies constitute a "clean" versus an "evil" file.
2. **Write the Filter**: Create a Python script at `/home/user/deploy_filter.py`. 
    - It must accept a single command-line argument: the absolute path to a configuration file.
    - It must evaluate the file and print exactly `ACCEPT` to standard output if the file is safe, or exactly `REJECT` if the file is malicious/malformed.
    - It must gracefully handle standard file parsing.
3. **Write the Integration Script**: Create a bash script at `/home/user/apply_config.sh`. This script must be idempotent. It should:
    - Create a directory `/home/user/deploy_service/`.
    - Generate a mock service configuration file `/home/user/deploy_service/config.ini` that includes the line `PreflightFilter=/home/user/deploy_filter.py`. If the line already exists, it should not duplicate it.
    - Start a mock background process (a simple `sleep infinity` looped in a script at `/home/user/deploy_service/mock_daemon.sh`) and log its PID to `/home/user/deploy_service/daemon.pid`. If the daemon is already running, it should restart it.

Your Python filter will be tested automatically against both the clean and evil corpora. It must achieve 100% accuracy.
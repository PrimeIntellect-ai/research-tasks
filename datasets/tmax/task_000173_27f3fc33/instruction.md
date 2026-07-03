You are a deployment engineer rolling out updates for a multi-service VM environment. 

You have two objectives to complete:

1. **Fix the Vendored Deployment Tool**
We use a custom tool called `vmm-deploy` to generate idempotent deployment scripts. The source code for version 0.5.0 is pre-vendored at `/app/vmm-deploy-0.5.0`.
However, the tool's `Makefile` was recently modified and now fails to build. You must debug and fix the `Makefile` or package configuration so that running `make install` successfully installs the `vmm-deploy` binary to `/home/user/.local/bin/vmm-deploy`. 

2. **Write a Configuration Validator**
Our deployment pipeline receives JSON configuration files defining application mounts and scheduled cron tasks. Some of these configurations are misconfigured or potentially malicious, attempting to mount sensitive host directories or run invalid cron schedules.
Write a Python script at `/home/user/validator.py` that accepts a single argument: the path to a deployment JSON file. 
The script must classify the file as safe or unsafe based on the following rules:
- **Mounts**: Every object in the `"mounts"` array has `"source"` and `"target"`. A configuration is EVIL if any `"source"` starts with `/etc`, `/var`, `/root`, or `/sys`. It is also EVIL if any `"target"` is located outside the `/home/user/app_data/` directory.
- **Cron**: The `"cron"` string must be exactly 5 space-separated fields. If it has fewer or more fields, the configuration is EVIL.

If the configuration violates any of these rules, the script must print exactly `EVIL` to standard output and exit with status code 1.
If the configuration follows all rules, the script must print exactly `CLEAN` to standard output and exit with status code 0.

Ensure your script is robust and correctly handles edge cases like nested paths (e.g., a target of `/home/user/app_data/../system/` is outside the allowed directory and thus EVIL).
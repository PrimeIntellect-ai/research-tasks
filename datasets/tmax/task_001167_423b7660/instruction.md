You are an infrastructure engineer tasked with diagnosing a failing systemd user service and writing a robust configuration linter.

We are deploying a new health-check and email alert routing daemon. The daemon is run via a systemd user service (`alert-router.service`), but it keeps failing to start in production. 

The service executes a proprietary, stripped C binary located at `/app/alert-router`. This binary reads email routing configuration files to set up monitoring endpoints and mailing list targets. Unfortunately, the vendor provided no documentation, and the binary is highly sensitive to the configuration file format—it often crashes or exits with a failure code when it encounters inputs it doesn't like.

Your objective is to:
1. Investigate the `/app/alert-router` binary (using reverse engineering or black-box testing) to deduce its validation rules and failure conditions. You have examples of crashing and working configs in `/home/user/example_configs/`.
2. Write a Python script at `/home/user/config_linter.py` that sanitizes and detects bad configurations before they are deployed to the daemon.

Requirements for `/home/user/config_linter.py`:
- It must be an executable Python script.
- It must accept exactly one argument: the path to a configuration file to analyze.
- Example invocation: `/home/user/config_linter.py /path/to/config.txt`
- If the configuration is safe and will be accepted by `/app/alert-router`, your script must exit with status code `0`.
- If the configuration will cause the binary to crash or reject it, your script must exit with status code `1` (or any non-zero value).
- It must run completely offline without actually invoking the `/app/alert-router` binary (the linter will be deployed to a CI pipeline where the binary is not present).

You must ensure your linter is accurate. An automated test suite will run your script against a large batch of hidden clean and malicious/crashing configuration files to verify your reverse-engineering efforts.
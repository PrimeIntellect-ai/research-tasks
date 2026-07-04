You are acting as a DevSecOps engineer implementing "policy as code" for a CI/CD pipeline. Developers frequently submit `sshd_config` files that are automatically parsed by a legacy shell script in the deployment pipeline. This legacy script is highly vulnerable to command injection.

Your task is to write a Python script that validates these SSH configuration files before they are accepted. 

First, examine the handwritten security memo provided as an image at `/app/policy_baseline.png`. You will need to extract the mandatory baseline SSH configuration settings written in that memo. (You can use `tesseract` which is pre-installed).

Next, create a validation script at `/home/user/validate_sshd.py`. This script will be invoked by our automated test suite as follows:
`python3 /home/user/validate_sshd.py <path_to_config_file>`

The script must implement the following logic:
1. **SSH Hardening Policy**: The parsed configuration file MUST exactly contain the key-value pairs specified in `/app/policy_baseline.png`. The matching should be case-insensitive for the keys, and tolerate arbitrary whitespace between the key and value.
2. **Injection Vulnerability Prevention**: Because the downstream CI tool uses an unsafe `eval`-like shell evaluation, the configuration file MUST NOT contain any of the following dangerous shell metacharacters anywhere in the file (even in comments): semicolons (`;`), pipes (`|`), ampersands (`&`), or backticks (`` ` ``).

**Exit conditions:**
- If the file meets ALL the SSH hardening baseline requirements AND contains NO dangerous shell metacharacters, your script must exit with status code `0`.
- If the file is missing a required baseline setting, has an incorrect value for a baseline setting, or contains any dangerous shell metacharacters, your script must exit with status code `1`.

Do not hardcode specific file names in your script; it must read the file path passed as the first command-line argument.
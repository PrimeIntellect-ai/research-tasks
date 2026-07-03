You are a Linux Systems Engineer tasked with hardening and automating configurations for a non-root environment. You need to accomplish two tasks related to configuration automation and storage monitoring.

Task 1: Automate Interactive Configuration
There is a legacy, interactive shell script located at `/home/user/setup/legacy_config.sh`. When run, it prompts the user interactively for locale and timezone settings before writing to a configuration file.
Your task is to write a robust automation script (in bash, python, or expect) at `/home/user/automate.sh` that automatically executes `/home/user/setup/legacy_config.sh` and provides the following answers to its prompts in order:
1. Timezone: `Etc/UTC`
2. Locale: `en_US.UTF-8`
3. Confirm: `y`
Execute your automation script so that the interactive script completes successfully and generates the resulting configuration file.

Task 2: Storage Monitoring Script
You must write a storage monitoring script at `/home/user/check_storage.sh` that calculates the total disk usage of the directory `/home/user/secure_storage` in kilobytes using `du -sk`.
- If the directory size is greater than or equal to 5000 KB, it should append the exact string `ALERT: secure_storage is <SIZE>KB` to `/home/user/storage_audit.log`.
- If the directory size is strictly less than 5000 KB, it should append `OK: secure_storage is <SIZE>KB` to `/home/user/storage_audit.log`.
(Where `<SIZE>` is the integer kilobyte size reported by `du -sk`).

Execute `/home/user/check_storage.sh` exactly once to generate the initial audit log entry.

Ensure your scripts handle execution cleanly. Both `/home/user/automate.sh` and `/home/user/check_storage.sh` must be executable and successfully run to complete the setup.
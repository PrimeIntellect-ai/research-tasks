You are acting as a cloud architect migrating a legacy service to a staged deployment model. We need to automate the cutover process using a Python script that manages directory structures and symlinks for atomic deployments.

I have set up the initial directory structure in `/home/user/migration/`. Inside, there are two version directories: `v1` and `v2`. There is also a global configuration file located at `/home/user/migration/config.json`.

Please write a Python automation script at `/home/user/deploy.py` that performs a staged deployment. The script should take exactly one command-line argument: the version to deploy (e.g., `v1` or `v2`). 

When executed (e.g., `python3 /home/user/deploy.py v2`), the script must do the following:
1. Create a symlink named `config.json` inside the specified version's directory (e.g., inside `/home/user/migration/v2/`) that points to the absolute path of the global config (`/home/user/migration/config.json`). Overwrite the symlink if it already exists.
2. Atomically update a global symlink located at `/home/user/app_current` to point to the absolute path of the specified version directory (e.g., `/home/user/migration/v2`).
3. Append a single line to a deployment log file located at `/home/user/deploy.log`. The line must exactly match this format:
`DEPLOYED <version> TO <absolute_target_path> WITH CONFIG <absolute_config_symlink_path>`
(For example: `DEPLOYED v2 TO /home/user/migration/v2 WITH CONFIG /home/user/migration/v2/config.json`)

Once you have written the script, use it to deploy version `v2`. Leave the system in this state so the deployment can be verified.
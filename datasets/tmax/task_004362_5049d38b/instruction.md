You are a container specialist managing microservices configuration for your team. 

Your team uses a Git-based workflow to manage configuration files. There is a central bare repository located at `/home/user/config_repo.git` and your local working clone is at `/home/user/config_workspace`.

Whenever new configurations are pushed to the central repository, a deployment script located at `/home/user/bin/deploy_configs.py` is supposed to deploy them. However, you are facing two major issues:
1. The script `deploy_configs.py` was written by a previous administrator. It interactively prompts for confirmation ("Apply changes? [y/N]: ") which causes standard Git hooks to hang.
2. Even when run manually, the script writes to the wrong location (`/tmp/default_deploy`) because Git hooks execute in a restricted environment where the custom `MICRO_DEPLOY_PATH` environment variable is missing.

Your objective is to fully automate this deployment pipeline by completing the following steps:

1. Create the target deployment directory: `/home/user/deployed_services`.
2. Write a Python script at `/home/user/bin/auto_answer.py` that acts as an Expect script. It must use the `pexpect` library to spawn `/home/user/bin/deploy_configs.py`, wait for the exact string `Apply changes? [y/N]: `, send `y` (followed by a newline), and then wait for the process to exit.
3. Create and configure the Git server hook at `/home/user/config_repo.git/hooks/post-receive` (ensure it has the correct executable permissions). The bash hook must:
    - Set and export the `MICRO_DEPLOY_PATH` environment variable to `/home/user/deployed_services`.
    - Execute `/usr/bin/python3 /home/user/bin/auto_answer.py` to trigger the deployment.
    - Read the standard input provided by Git to a `post-receive` hook (which format is: `<oldrev> <newrev> <refname>`).
    - Use a text processing pipeline (`git diff-tree`, `grep`, `awk`, `sed`, etc.) to find all files ending in `.yml` that were added or modified in the push.
    - For each `.yml` file found, extract *only* the base name without the extension (e.g., if `networking/routes.yml` was changed, extract `routes`) and append this string to `/home/user/hook_metrics.log`, one per line.
4. Finally, verify your pipeline: Inside your local clone at `/home/user/config_workspace`, create a file named `inventory.yml` (content does not matter), commit it to the `master` branch, and push it to `origin`.

If everything is configured correctly, the push will succeed automatically without hanging, the deployment script will write its success flag to the correct directory, and the metrics log will be updated.
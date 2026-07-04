You are a Linux systems engineer responsible for hardening our deployment pipeline. We have a local Git repository that serves as our deployment origin, but we want to prevent deployments (pushes) if our application's configuration file isn't properly secured.

Here is your task:

1. A bare Git repository exists at `/home/user/deploy.git`. 
2. Our application configuration file is located at `/home/user/app_config.json`. 
3. Write a Git `pre-receive` hook in Go. Save your source code at `/home/user/pre-receive.go` and compile it to exactly `/home/user/deploy.git/hooks/pre-receive`. Ensure the compiled binary is executable.
4. The Go hook must perform a deployment health check by verifying the file permissions of `/home/user/app_config.json`.
   - It must read the standard `pre-receive` input from stdin (lines formatted as `<old-value> <new-value> <ref-name>`).
   - If the permissions of `/home/user/app_config.json` are strictly `0600` (`-rw-------`), the hook must exit with status code `0` to allow the deployment.
   - If the permissions are anything else, the hook must print exactly `Hardening check failed: app_config.json permissions are too open\n` to standard error, and exit with status code `1` to reject the deployment.
5. Fix the permissions on `/home/user/app_config.json` so that they are securely set to `0600`.
6. To verify your setup, clone the bare repository to `/home/user/workspace`, create a file named `deploy.txt` with the text `init`, commit it, and push it to the `master` branch.
7. Redirect the combined standard output and standard error of your `git push` command to `/home/user/push_result.log`.

Do not use root privileges; assume all work is done as the user `user`.
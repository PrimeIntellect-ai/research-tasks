You are an observability engineer tuning the deployment pipeline for your custom dashboarding solution. You want to automate the deployment of dashboard JSON configuration files using Git.

You have a bare Git repository located at `/home/user/dashboard-repo.git`.
Whenever new dashboard configurations are pushed to this repository, they need to be automatically deployed and the dashboard service needs to be informed to reload them.

Your task is to create a Git `post-receive` hook that accomplishes the following:

1. **Deploy Files**: Checkout the latest `master` branch from the bare repository into the working directory `/home/user/dashboards_deployed`.
2. **Manage Permissions**: Ensure the deployed files and directory have restricted permissions. The directory `/home/user/dashboards_deployed` and all files within it must have permissions set to `750` (read/write/execute for owner, read/execute for group, no access for others).
3. **Service Lifecycle Management**: Our mock dashboard service runs in the background and writes its Process ID to `/home/user/dashboard.pid`. Your hook must send a `SIGHUP` signal to the process ID found in this file to trigger a dashboard reload.
4. **Audit Logging**: Append a log entry to `/home/user/deploy.log` using the exact format: `[YYYY-MM-DD HH:MM:SS] Dashboards reloaded` (e.g., `[2023-10-25 14:30:00] Dashboards reloaded`).

Make sure your hook script is written in Bash, is executable, and is placed in the correct location for the bare Git repository. Do not perform any git pushes yourself; simply set up the hook and its required components.
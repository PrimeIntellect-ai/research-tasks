You are a deployment engineer rolling out a new update mechanism. Our automated deployment pipeline relies on a user-level systemd service (`deploy-worker.service`) that watches a local Git repository, but it is currently failing to start reliably and the deployment paths are broken.

Please fix the following issues in the `/home/user` environment:

1. **Directory and Link Management**: 
   The symlink at `/home/user/active-deployment` is currently pointing to a deleted release directory (`/home/user/releases/v1`). Recreate or update this symlink so that it points to the new release directory at `/home/user/releases/v2`.

2. **Git Hook Configuration**:
   We have a local bare Git repository at `/home/user/project.git`. The post-receive hook located at `/home/user/project.git/hooks/post-receive` has been created but is not triggering. Ensure this file has the correct permissions to be executed by the Git daemon.

3. **Service Lifecycle Management**:
   The worker service `/home/user/.config/systemd/user/deploy-worker.service` frequently fails on boot because it attempts to start before the local Git server (`git-daemon.service`) is ready. 
   - Modify the `deploy-worker.service` file to add `git-daemon.service` to the `After=` directive in the `[Unit]` section.
   - Reload the user systemd daemon to apply the changes.
   - Start and enable the `deploy-worker.service` using `systemctl --user`.

Do not use root/sudo, as everything is configured in your local user space (`systemctl --user`).
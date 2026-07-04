You are an SRE monitoring the uptime and deployment metrics for our internal systems. We have a localized metrics collection setup located in `/app/metrics_stack/`. A startup script (`/app/metrics_stack/start.sh`) brings up two services:
1. A user-space SSH daemon running on `127.0.0.1:2222` serving a bare Git repository located at `/home/user/git-server/repo.git`.
2. A local HTTP Metrics Server running on `10.0.0.5:8080` (bound to a dummy interface).

Currently, this system is broken in a few ways:
1. The SSH daemon silently rejects key-based logins for the `user` account using the key located at `/home/user/.ssh/id_rsa`. The daemon is using the configuration file at `/home/user/sshd_config`. You must fix this configuration so that public key authentication works.
2. The Git repository is supposed to report deployment events to the Metrics Server whenever new commits are pushed. You must create a `post-receive` Git hook in `/home/user/git-server/repo.git/hooks/post-receive`. This hook must execute a simple bash script that sends an HTTP POST request to `$METRICS_URL/push` with the payload `event=pushed`.
3. The `$METRICS_URL` environment variable must be properly resolved when the Git hook runs during an SSH session. You must configure the appropriate shell profile or SSH environment setup for the `user` so that `$METRICS_URL` evaluates to `http://10.0.0.5:8080` during the non-interactive SSH session triggered by a `git push`.
4. The local dummy network interface `metric0` does not currently have the correct routing to reach `10.0.0.5`. You must add the necessary routing configuration using standard `ip` commands so that `10.0.0.5` is reachable from the local environment.

Once you have fixed the SSH configuration, created the hook, set up the environment variables, and fixed the local route, restart the SSH daemon (by killing the process and letting the start script/agent manage it, or running `/usr/sbin/sshd -f /home/user/sshd_config`).
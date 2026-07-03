You are a deployment engineer responsible for rolling out the `v2` update of our internal Go service. You must execute a staged deployment that involves writing the new service, automating its interactive startup, verifying connectivity, updating symlinks, and generating an email notification. 

All work must be done within `/home/user`. 

Complete the following phases:

**Phase 1: Write the Go Service**
Write a Go web service at `/home/user/src/app_v2.go` and compile it to `/home/user/deploy/v2/app`.
The service must:
1. Prompt exactly `Enter deployment key: ` on standard output upon startup and wait for standard input.
2. If the input is exactly `rollout-2024`, the application should start an HTTP server on `127.0.0.1:8080`.
3. If the input is wrong, it should exit with status 1.
4. The HTTP server must respond to `GET /status` with the exact plaintext body `OK-v2`.

**Phase 2: Interactive Automation Script**
Write an Expect script (or Bash script using `expect` inline) at `/home/user/scripts/start_service.exp`.
This script must:
1. Execute `/home/user/deploy/v2/app`.
2. Wait for the `Enter deployment key: ` prompt.
3. Provide the key `rollout-2024`.
4. Leave the service running in the background (you may use standard expect daemonization or shell backgrounding techniques around the expect script).

**Phase 3: Staged Rollout & Connectivity Diagnostics**
Write a Bash script at `/home/user/scripts/deploy.sh` that performs the actual rollout:
1. Execute `/home/user/scripts/start_service.exp` to start the `v2` app.
2. Use a loop with `curl` or `nc` to check `http://127.0.0.1:8080/status` until it responds or 10 seconds pass.
3. If it successfully responds with `OK-v2`, update the deployment symlink: atomically change `/home/user/deploy/current` (which currently points to `/home/user/deploy/v1`) to point to `/home/user/deploy/v2`.

**Phase 4: Email Notification**
If the deployment (symlink swap) succeeds, the `deploy.sh` script must drop an email file simulating local delivery into the local Maildir structure at `/home/user/mail/new/`.
The file must be named `deployment_report.eml` and contain the following exact structure:
```
To: team@local
From: deploy@local
Subject: Deployment Success

Service v2 is live.
```

Execute your `deploy.sh` script so the final state is achieved: the `v2` app is running, the `current` symlink is updated, and the email file exists.
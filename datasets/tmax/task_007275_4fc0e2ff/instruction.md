You are a deployment engineer tasked with rolling out an update for an internal application. Your goal is to configure a local Git deployment pipeline, set up a Go-based email notification script, and redirect network traffic to the new version using user-space port forwarding.

Perform the following tasks:

1. **Git Hook Configuration:**
   A bare Git repository exists at `/home/user/app.git`. Configure a `post-receive` hook for this repository (`/home/user/app.git/hooks/post-receive`). 
   The hook must be executable and strictly perform the following actions when a push is received:
   - Read the standard input provided by Git (which is formatted as `<old-hash> <new-hash> <ref-name>`).
   - Execute the Go script `/home/user/notify.go` (which you will create), passing the new commit hash as the first command-line argument.

2. **Go Notification Script:**
   Write a Go program at `/home/user/notify.go`. The program must:
   - Accept the new commit hash as the first command-line argument (`os.Args[1]`).
   - Create a simulated email file in the `/home/user/mail/` directory named `deployed_<new-hash>.eml`.
   - The contents of this file must be exactly:
     ```
     To: dev@local
     Subject: Update rolled out
     
     Commit: <new-hash>
     ```

3. **Traffic Redirection (Port Forwarding):**
   The new deployment runs on port 9090, but current traffic arrives on port 8080. Since you do not have root access for `iptables`, use `socat` to forward TCP traffic from port 8080 to localhost:9090.
   - Start this process in the background.
   - Save the PID of the background `socat` process to `/home/user/port_forward.pid`.

4. **Trigger the Deployment:**
   A local clone of the repository exists at `/home/user/source`. 
   Navigate to `/home/user/source`, create an empty commit with the exact message `Trigger rollout`, and push the `main` branch to the `origin` remote to trigger the hook.

Ensure all paths, formats, and filenames match exactly, and do not use root/sudo privileges.
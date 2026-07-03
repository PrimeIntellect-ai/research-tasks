You are a deployment engineer tasked with building a custom, lightweight Continuous Deployment (CD) service in C. The service will run as a user-level daemon, listen for triggers from a Git `post-receive` hook, enforce simulated user authorization, and deploy authorized updates. 

Since you do not have root access, you will configure everything within your home directory (`/home/user`).

Here are the exact requirements:

**1. The Authorization Roster**
Create a file at `/home/user/authorized_deployers.txt`. Add the following authorized deployer emails, one per line:
`alice@example.com`
`bob@example.com`

**2. The Deployment Daemon (C Program)**
Write a C program at `/home/user/deploy_daemon.c` and compile it to `/home/user/deploy_daemon` (ensure it has executable permissions).
The daemon must continuously do the following:
* Create and listen on a Unix domain socket at `/home/user/deploy.sock`. (Make sure to `unlink()` it before binding if it already exists).
* Accept incoming connections. Once a client connects, read exactly one line containing a 40-character Git commit hash.
* For each received commit hash:
  1. Determine the author's email of that commit within the bare repository at `/home/user/deploy_repo.git`. You can invoke a shell command like `git -C /home/user/deploy_repo.git show -s --format='%ae' <hash>`.
  2. Check if the retrieved email exists in `/home/user/authorized_deployers.txt`.
  3. If the user **is authorized**:
     - Deploy the files from that commit to `/home/user/live_site/` (create this directory beforehand). You can use `git archive` piped to `tar`.
     - Append the exact string `SUCCESS: <hash> by <email>\n` to `/home/user/deploy.log`.
  4. If the user **is NOT authorized**:
     - Do NOT deploy the files.
     - Append the exact string `DENIED: <hash> by <email>\n` to `/home/user/deploy.log`.
* Continue listening for the next connection.

**3. Service Lifecycle Management**
Manage the C daemon using a user-level `systemd` service.
* Create a unit file at `/home/user/.config/systemd/user/deploy-daemon.service`.
* The service must execute `/home/user/deploy_daemon`.
* Ensure it runs in the background. Reload the user systemd daemon (`systemctl --user daemon-reload`), enable the service, and start it.

**4. The Git Server and Hook**
* Initialize a bare Git repository at `/home/user/deploy_repo.git`.
* Write an executable `post-receive` hook inside `/home/user/deploy_repo.git/hooks/post-receive`.
* When a push occurs, the `post-receive` hook reads standard input (which Git provides in the format: `<oldrev> <newrev> <refname>`).
* The hook must extract the `<newrev>` (the new commit hash) and send it to the Unix socket `/home/user/deploy.sock`. (You can use a tool like `nc -U`, `socat`, or a short Python/Bash inline script to write to the socket).

Complete all configuration, code writing, compilation, and service launching. Ensure the service is running and listening on the socket when you are finished.
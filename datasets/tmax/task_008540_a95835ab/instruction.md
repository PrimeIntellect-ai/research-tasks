You are tasked with setting up a lightweight, automated deployment pipeline using Git hooks. We need a continuous deployment mechanism that manages a Python web service without relying on root privileges or a formal init system like systemd.

System state and requirements:
1. There is a bare Git repository at `/home/user/app.git`.
2. There is a local development workspace at `/home/user/workspace` which is a Git repository configured with `origin` pointing to `/home/user/app.git`.
3. Inside `/home/user/workspace`, there is a Python application named `server.py` that listens on `localhost:8080`.

Your objective is to write a Git `post-receive` hook in Python and trigger a deployment.

Step 1: Write the Hook
Create a Python 3 executable script at `/home/user/app.git/hooks/post-receive`. When a push is made to the `main` branch, this hook must:
- Extract the pushed code into `/home/user/deploy`. (You can use `git --work-tree=/home/user/deploy --git-dir=/home/user/app.git checkout -f main`).
- Read the file `/home/user/deploy/server.pid`. If it exists and contains a valid process ID, terminate that old process.
- Start `/home/user/deploy/server.py` as a background process using `python3`.
- Write the new process ID to `/home/user/deploy/server.pid`.
- Log the message "Deployment successful" to `/home/user/deploy.log`.

Step 2: Trigger the Pipeline
- Commit the `server.py` file in `/home/user/workspace` to the `main` branch.
- Push the `main` branch to the `origin` repository (`/home/user/app.git`).

Ensure that by the end of your tasks, the `post-receive` hook has executed, the Python server is actively running on port 8080 in the background, and the `server.pid` file accurately reflects the running process ID.
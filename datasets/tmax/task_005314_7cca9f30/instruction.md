You are an infrastructure engineer setting up a lightweight "push-to-deploy" pipeline. You need to configure a local bare Git repository that uses a Python-based hook to automatically generate a load balancer configuration file and log the deployment lifecycle.

Perform the following steps:

1. Create a bare Git repository at `/home/user/deploy.git`.
2. Write a Git `post-receive` hook written in Python 3 at `/home/user/deploy.git/hooks/post-receive`. Ensure it is executable.
3. The Python hook must do the following on every push:
   - Read the standard input provided by Git (`<oldrev> <newrev> <refname>`).
   - Read a configuration file located at `/home/user/ports.conf`. This file will contain a single line of comma-separated port numbers (e.g., `8001,8002`). If the file does not exist, assume a default single port of `8080`.
   - Generate a load balancer configuration file at `/home/user/proxy.json` in the following exact JSON format (indented by 2 spaces), dynamically populated with the ports read in the previous step:
     ```json
     {
       "mode": "round-robin",
       "backend_servers": [
         "http://127.0.0.1:8001",
         "http://127.0.0.1:8002"
       ]
     }
     ```
   - Append a log entry to `/home/user/deploy.log` with the exact format:
     `SUCCESS: Commit <newrev> deployed across <N> containers.` 
     (Where `<newrev>` is the full commit hash from stdin, and `<N>` is the number of ports/backend servers).
4. Create the file `/home/user/ports.conf` with the following content: `9001,9002,9003`
5. Clone the bare repository to `/home/user/workspace`.
6. Inside `/home/user/workspace`, create a file named `app.py` with the text `print("Hello World")`, commit it to the `master` branch, and push it to the `origin` (the bare repository) to trigger the hook.

Ensure that by the end of your task, `/home/user/proxy.json` and `/home/user/deploy.log` are successfully created by the hook.
You are a monitoring specialist tasked with setting up an automated alerting system using Git hooks. 

We manage our monitoring targets in a Git repository. Whenever someone pushes changes to the repository, we want to immediately verify if the newly configured endpoints are actually reachable. Sometimes endpoints are added that silently reject connections, and we want to catch this immediately.

Your task is to implement this workflow:

1. There is a bare Git repository at `/home/user/targets.git`.
2. There is a working clone of this repository at `/home/user/targets_work`.
3. Create a Git `post-receive` hook in the bare repository (`/home/user/targets.git/hooks/post-receive`). The hook must be written entirely in Python 3.
4. The hook must do the following when a push occurs:
   - Read the standard input provided by Git (`oldrev newrev refname`).
   - Identify all `.json` files present in the repository at the `newrev` commit.
   - For each `.json` file, parse its contents. The JSON files will always have this structure:
     `{"endpoints": [{"host": "127.0.0.1", "port": 8080}, {"host": "127.0.0.1", "port": 8081}]}`
   - For every endpoint listed in every `.json` file, attempt to establish a TCP connection to the specified `host` and `port` (use a 1-second timeout).
   - If the TCP connection fails (e.g., Connection Refused or Timeout), append an alert to the log file exactly at `/home/user/alerts.log`.
   - The log line must exactly match this format: `ALERT: Cannot connect to {host}:{port}` (e.g., `ALERT: Cannot connect to 127.0.0.1:8081`). Do not log successful connections.

5. After creating and enabling the hook, test it:
   - In your working clone (`/home/user/targets_work`), create a file named `services.json`.
   - Add the following content to `services.json`:
     `{"endpoints": [{"host": "127.0.0.1", "port": 10000}, {"host": "127.0.0.1", "port": 10001}]}`
   - Start a simple listening service on port 10000 in the background (e.g., using `python3 -m http.server 10000 &`). Ensure port 10001 remains closed.
   - Commit and push the `services.json` file to the bare repository's `master` branch.

If your setup is correct, the push will trigger the hook, the hook will test the endpoints, port 10000 will succeed silently, port 10001 will fail, and the failure will be logged to `/home/user/alerts.log`.
You are an observability engineer tuning the dashboard deployment pipeline. We track our Grafana dashboard JSON configurations in a local bare Git repository. You need to set up a system that automatically notifies our simulated alerting service whenever a dashboard is updated.

Follow these instructions exactly:

1. **Create the Alert Service (Rust):**
   - Create a new Rust project at `/home/user/alert_service`.
   - Write a Rust program that listens for TCP connections on `127.0.0.1:2525`.
   - For every connection, it should read the incoming UTF-8 string. If the string starts with `ALERT: `, it should append the entire string (stripped of trailing newlines, then adding exactly one newline) to `/home/user/dashboard_alerts.log`.
   - Build the release binary.
   - Start the service in the background and save its process ID to `/home/user/alert_service.pid`.

2. **Configure the Git Repository:**
   - Initialize a bare Git repository at `/home/user/dashboards.git`.
   - Create a `post-receive` hook at `/home/user/dashboards.git/hooks/post-receive`.
   - The hook must be a bash script. When triggered, it should read the oldrev, newrev, and refname from stdin (standard `post-receive` behavior).
   - It should use `git diff-tree` to check if any files ending in `.json` were modified or added in the pushed commits.
   - If a `.json` file was changed, the hook must send the exact string `ALERT: Dashboards updated` to `127.0.0.1:2525` (you can use `nc` for this).
   - Ensure the hook has the correct execution permissions.

3. **Test the Pipeline:**
   - Clone the bare repository to `/home/user/dashboards_work`.
   - Create a file named `network_dashboard.json` with the content `{"title": "Network Metrics"}`.
   - Commit and push the changes back to the bare repository (`origin master`).

After completing these steps, the automated test will check the contents of `/home/user/dashboard_alerts.log` and verify the hook permissions and service lifecycle state.
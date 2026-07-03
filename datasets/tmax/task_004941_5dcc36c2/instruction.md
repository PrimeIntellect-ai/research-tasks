You are tasked with setting up a highly available, user-space application cluster with automated storage monitoring. You do not have root access, so all configurations must run under the user environment (`/home/user`).

Here is what you need to build:

1. **Backend Application**: 
   Write a Python script `/home/user/backend.py` that takes a port number as a command-line argument. It should run an HTTP server on `127.0.0.1` at that port. When it receives a POST request to `/upload`, it should read the body and append it to a file at `/home/user/app_data/backend_<port>.dat`. It should return a `200 OK` response with the text `OK from <port>`.

2. **Reverse Proxy / Load Balancer**:
   Write a Python script `/home/user/lb.py` that listens on `127.0.0.1:8080`. It should act as a round-robin load balancer, forwarding incoming HTTP POST requests to 3 backend instances running on ports `8081`, `8082`, and `8083`. It must return the exact response received from the backend.

3. **Storage Monitoring**:
   Write a Python script `/home/user/monitor.py` that continuously checks the total size of all files in `/home/user/app_data/` every 2 seconds. 
   If the total size of files in this directory exceeds 1 MB (1,048,576 bytes), the script must:
   - Identify the largest `.dat` file in the directory.
   - Delete that file.
   - Append a line to `/home/user/alert.log` in this exact format: `[YYYY-MM-DD HH:MM:SS] ALERT: Quota exceeded. Deleted <filename>` (where `<filename>` is just the name of the file, e.g., `backend_8081.dat`).

4. **Process Supervision**:
   Create a `supervisord` configuration file at `/home/user/supervisord.conf`. 
   Configure it to manage and supervise:
   - The 3 backend instances (on ports 8081, 8082, 8083)
   - The load balancer (`lb.py`)
   - The storage monitor (`monitor.py`)
   All managed processes must be configured to automatically restart if they crash. Configure `supervisord` to run in the foreground or background, but ensure the agent starts it so it's running when you finish the task. Log files for supervisor itself should be placed in `/home/user/supervisor_logs/`.

**Initial Setup Steps for you**:
- Create `/home/user/app_data/` and `/home/user/supervisor_logs/` directories.
- Write the required Python scripts.
- Write the `supervisord.conf` file.
- Start `supervisord` using your configuration (`supervisord -c /home/user/supervisord.conf`).

Leave `supervisord` and all processes running as your final state.
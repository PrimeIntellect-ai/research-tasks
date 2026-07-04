You are tasked with building a lightweight "Kubernetes-like operator" that manages process lifecycles based on declarative manifests, runs on a schedule, and sends notifications via a local mail spool.

Here are the requirements:

1. **Manifest Parsing**: 
   You must write a script located at `/home/user/operator.sh` (or any other language, e.g., `/home/user/operator.py`). 
   It should read all `.json` files in the directory `/home/user/manifests/`. Each JSON file represents a service and has the following format:
   ```json
   {
     "service_name": "worker-alpha",
     "command": "sleep 3600",
     "replicas": 2
   }
   ```

2. **Process Lifecycle Management**:
   For each manifest, your operator must ensure that exactly the requested number of `replicas` (instances of the command) are currently running in the background.
   - To keep track of running processes, your operator must store the Process IDs (PIDs) for each service in a file located at `/home/user/run/<service_name>.pids` (one PID per line).
   - If there are fewer running processes than the `replicas` count, the operator must start new instances of the `command` in the background and record their new PIDs.
   - If there are more running processes than the `replicas` count, the operator must terminate (SIGTERM) the excess processes (specifically, the ones most recently started / at the bottom of the pids file) and remove them from the PID file.
   - Dead processes (PIDs in the file that are no longer running) should be cleaned up from the PID file before calculating how many new instances to start.

3. **Email Notification System**:
   Whenever the operator starts or terminates a process, it must simulate sending an email by appending a message in standard mbox format to `/home/user/mail/admin`. 
   The email must have:
   - `From: operator@localhost`
   - `To: admin@localhost`
   - `Subject: Scaling service <service_name>`
   - The body should contain exactly one line per action: either `Started PID <pid>` or `Terminated PID <pid>`.
   *(If multiple actions happen in one run for a service, they can be grouped into one email or sent as separate emails, as long as the format is valid mbox).*

4. **Scheduled Task**:
   Set up a user cron job (`crontab`) that executes your operator script exactly once every minute. 

Before finishing the task:
- Ensure `/home/user/manifests/` and `/home/user/run/` and `/home/user/mail/` directories exist.
- Create a test manifest `/home/user/manifests/test-service.json` with `service_name: "test-service"`, `command: "sleep 7200"`, and `replicas: 3`.
- Run your operator script at least once manually so that the processes are spawned, the `.pids` file is created, and the initial email notification is written.
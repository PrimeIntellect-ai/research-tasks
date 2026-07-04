You are a site administrator tasked with building a robust, self-healing deployment for a background service that provisions user accounts and sends welcome emails. Since we don't have root access to systemd, you must build a custom process supervisor in bash to manage a worker daemon written in Go.

Your objective is to complete the following:

1. **Directories**: Create the following directories:
   - `/home/user/requests` (where incoming account requests will be placed)
   - `/home/user/mail/outbox` (where outgoing welcome emails will be written)

2. **The Go Worker**: Write a Go program at `/home/user/worker.go` and compile it to `/home/user/worker`.
   The worker must:
   - Run in an infinite loop, checking for new `.json` files in the directory specified by the `PROVISION_DIR` environment variable every 1 second.
   - For every `.json` file found, read it. The JSON will have the format: `{"username": "<string>", "email": "<string>", "crash": <boolean>}`. (The "crash" key is optional).
   - If the key `"crash"` is `true`, the Go program MUST immediately panic and exit with a non-zero exit code (do not process the file or delete it).
   - Otherwise, generate an email file in the directory specified by the `OUTBOX_DIR` environment variable. The file must be named `<username>.eml`.
   - The contents of the `.eml` file must be exactly:
     ```
     From: <value of FROM_EMAIL env var>
     To: <email from json>
     Subject: Welcome to the system, <username from json>

     Your account has been provisioned.
     ```
   - After successfully creating the `.eml` file, the worker must delete the `.json` file.

3. **The Supervisor**: Write a bash script at `/home/user/supervisor.sh` that:
   - Exports the necessary environment variables: 
     - `PROVISION_DIR=/home/user/requests`
     - `OUTBOX_DIR=/home/user/mail/outbox`
     - `FROM_EMAIL=admin@system.local`
   - Starts the compiled `/home/user/worker` program.
   - Monitors the worker. If the worker exits for any reason (e.g., it crashes), the supervisor must automatically restart it.

4. **Execution**: 
   - Start your supervisor script in the background.
   - Save the Process ID (PID) of the *supervisor script itself* into a file located at `/home/user/supervisor.pid`.

Make sure the Go program handles basic errors (like an invalid JSON file structure) gracefully without crashing, unless explicitly told to crash via the `"crash": true` field. Do not leave the supervisor running in the foreground; it must be detached so you can complete the task and return the prompt.
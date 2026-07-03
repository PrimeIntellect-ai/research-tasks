You are a monitoring specialist tasked with setting up an automated custom alert system. You have been given an image containing a secret access token, and you need to build the pipeline that collects, commits, and displays alerts.

Here are the requirements:

1. **Extract the Token**:
   There is an image at `/app/token.png` that contains the secret alert token. Extract this token to use in the subsequent steps. Tesseract is installed on the system.

2. **Alert Dashboard Server**:
   Write and start a Python HTTP server that runs continuously, listening on `127.0.0.1:8000`. The server must implement the following endpoints:
   - `GET /status`: Returns a JSON response `{"status": "ok", "tz": "<timezone>", "locale": "<locale>"}`. The timezone and locale should reflect the environment variables `TZ` and `LANG` of the running server.
   - `POST /alert`: Accepts a JSON payload like `{"level": "CRITICAL", "message": "High CPU"}`. It must require the HTTP header `Authorization: Bearer <TOKEN>` (using the token from the image). If authorized, it stores the alert in memory and returns `200 OK`. If unauthorized, return `401`.
   - `GET /alerts`: Returns a JSON list of all stored alerts (e.g., `[{"level": "CRITICAL", "message": "High CPU"}]`). Also requires the `Authorization: Bearer <TOKEN>` header.

3. **Locale and Timezone Configuration**:
   Ensure your Alert Dashboard server runs with the timezone set to `Europe/Berlin` and the locale set to `de_DE.UTF-8`.

4. **Git Server and CI/CD Hook**:
   - Create a bare Git repository at `/home/user/alerts.git`.
   - Create a `post-receive` hook in this bare repository (written in Python or Bash).
   - The hook acts as a simple CI/CD pipeline: whenever a new commit is pushed, the hook should read the names of the added or modified files. For any file ending in `.alert`, the hook must read its contents (which will be in the format `LEVEL:MESSAGE`, e.g., `CRITICAL:Disk Full`) and send a `POST /alert` request to your Alert Dashboard at `127.0.0.1:8000` using the secret token. 

5. **Automated Submission via Expect**:
   There is an interactive script at `/app/interactive_submit.sh` (you don't need to create this, assume it exists and is executable) that asks three interactive questions:
   - `Enter local repo path:` 
   - `Enter alert level:`
   - `Enter alert message:`
   After answering, the script creates a file named `alert_<timestamp>.alert` with the level and message, commits it to the local repo, and pushes to origin.
   - You must write an Expect script at `/home/user/auto_alert.exp` that automates calling `/app/interactive_submit.sh`. It should provide `/home/user/alerts_local` for the repo path, `WARNING` for the alert level, and `Memory usage high` for the alert message.
   - Note: You must initialize the local git clone at `/home/user/alerts_local` yourself, pointing its origin to `/home/user/alerts.git`.

6. **Scheduled Task**:
   Configure a cron job for the `user` to run the Expect script (`/home/user/auto_alert.exp`) every 5 minutes. 

Ensure the Python server is running in the background before you finish the task.
You are a system administration specialist setting up a new monitoring and alerting pipeline. A previous admin left behind a screenshot of the alerting configuration, but the original setup scripts were lost. Furthermore, the local storage quota checker now strictly requires interactive password authentication.

Your objective is to reconstruct the monitoring service and its required interactive automation.

Step 1: Configuration Extraction
There is an image at `/app/alert_config.png` containing the required configuration. Extract the `PORT` and `TOKEN` values from this image. 

Step 2: Interactive Automation
The local storage monitoring tool is located at `/app/secure_quota_check.sh`. Because of a broken key-based auth configuration, this script now prompts interactively for a password ("Enter monitoring password: "). 
Write an `expect` script that automates the execution of `/app/secure_quota_check.sh` using the password `mon_alert_99`. Your `expect` script should capture and output the underlying tool's standard output (which looks like `DISK_USAGE=<number>`).

Step 3: Alerting Web Service
Develop a web server (using any language of your choice) that acts as the monitoring daemon. The server must listen on `127.0.0.1` on the `PORT` you extracted from the image.
It must implement the following two HTTP endpoints:

1. `GET /poll`
   When this endpoint is hit, your server must execute your `expect` script, parse the resulting disk usage integer, and return a JSON response in the exact format:
   `{"status": "success", "usage": <integer>}`

2. `POST /alert`
   This endpoint receives alerting payloads. It MUST enforce HTTP Bearer token authentication using the exact `TOKEN` extracted from the image (`Authorization: Bearer <TOKEN>`). 
   If the token is missing or invalid, return a `401 Unauthorized`.
   If the token is valid, append the raw POST request body (JSON) as a new line to `/home/user/alerts.log`, and return a `200 OK`.

Ensure your server is running in the background and is fully functional before concluding your work. Do not output the extracted token or port in your final message.